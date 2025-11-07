import os
import stripe
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Plan, Subscription
from dotenv import load_dotenv
from .invoice_generator import generate_invoice_pdf

load_dotenv()

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_checkout_session(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    user = request.user

    existing_customer = stripe.Customer.list(email=user.email).data
    if existing_customer:
        customer_id = existing_customer[0].id
    else:
        customer = stripe.Customer.create(email=user.email)
        customer_id = customer.id

    session = stripe.checkout.Session.create(
        customer=customer_id,
        payment_method_types=['card'],
        line_items=[{
            'price': plan.stripe_price_id,
            'quantity': 1,
        }],
        mode='subscription',
        success_url=os.getenv('DOMAIN') + '/plans/',
        cancel_url=os.getenv('DOMAIN') + '/plans/',
    )

    return JsonResponse({'url': session.url, 'sessionId': session.id})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv('STRIPE_WEBHOOK_SECRET')
        )
    except Exception as e:
        return HttpResponse(status=400)

    try:
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            customer_id = session.get('customer')
            subscription_id = session.get('subscription')
            email = session.get('customer_email')

            if not email and customer_id:
                customer = stripe.Customer.retrieve(customer_id)
                email = customer.email
        
            if not (email and customer_id and subscription_id):
                return HttpResponse(status=200)

            user = User.objects.filter(email=email).first()
            if not user:
                return HttpResponse(status=404)

            sub_data = stripe.Subscription.retrieve(subscription_id)
            price_id = sub_data['items']['data'][0]['price']['id']
            plan = Plan.objects.filter(stripe_price_id=price_id).first()

            if not plan:
                return HttpResponse(status=404)

            Subscription.objects.create(
                user=user,
                plan=plan,
                stripe_customer_id=customer_id,
                stripe_subscription_id=subscription_id,
                status='active',
                is_active=True,
            )
            generate_invoice_pdf(user,plan)
      

        elif event['type'] == 'invoice.payment_succeeded':

            invoice = event['data']['object']
            subscription_id = invoice.get('subscription')

            if not subscription_id:
                return HttpResponse(status=200)

            subscription = Subscription.objects.filter(stripe_subscription_id=subscription_id).first()
            if subscription:
                subscription.status = 'active'
                subscription.is_active = True
                subscription.save()

        elif event['type'] == 'customer.subscription.deleted':
            sub_data = event['data']['object']
            sub_id = sub_data.get('id')

            subscription = Subscription.objects.filter(stripe_subscription_id=sub_id).first()
            if subscription:
                subscription.status = 'canceled'
                subscription.is_active = False
                subscription.save()

        elif event['type'] == 'invoice.payment_failed':
            sub_data = event['data']['object']
            subscription_id = sub_data.get('subscription')

            subscription = Subscription.objects.filter(stripe_subscription_id=subscription_id).first()
            if subscription:
                subscription.status = 'expired'
                subscription.is_active = False
                subscription.save()

    except Exception as e:
        import traceback
        traceback.print_exc()
        return HttpResponse(status=500)

    return HttpResponse(status=200)
