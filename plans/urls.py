from django.contrib import admin
from django.urls import path, include
from .views import PlanList, SubscriptionCreate,UserSubscriptionDetail
from .stripe import create_checkout_session, stripe_webhook

urlpatterns = [
   path('plans/',PlanList.as_view(),name='plans-list'),
   path('plans/<int:pk>/subscription-create/',SubscriptionCreate.as_view(),name='subscription-create'),
   path('user-subscription/',UserSubscriptionDetail.as_view(),name='user-subscription'),
   path('create-checkout-session/<int:plan_id>/', create_checkout_session, name='create-checkout-session'),
   path('api/webhook/', stripe_webhook),
]
