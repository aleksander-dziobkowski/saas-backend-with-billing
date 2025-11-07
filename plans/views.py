from rest_framework.views import APIView
from rest_framework import status,generics,mixins,viewsets
from .serializers import PlanSerializer, SubscriptionSerializer
from .models import Plan,Subscription
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
import stripe

class PlanList(generics.ListAPIView):
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()
    ordering_fields = ['price']
    
class UserSubscriptionDetail(generics.RetrieveDestroyAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]   

    def get_object(self):
        return get_object_or_404(Subscription, user=self.request.user, is_active=True)
    
    def perform_destroy(self, instance):
        stripe.Subscription.delete(instance.stripe_subscription_id)
        instance.status = 'canceled'
        instance.is_active = False
        instance.save()
