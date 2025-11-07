import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Plan,Subscription
from rest_framework_simplejwt.tokens import RefreshToken
from unittest.mock import patch

@pytest.mark.django_db
def test_plans_list(client):
    url = reverse('plans-list')
    response = client.get(url)
    assert response.status_code in [200]
    
@pytest.mark.django_db
def test_subscription_create(client,django_user_model):
    user = django_user_model.objects.create_user(username='test123',email="test@example.com", password="StrongPass123")
    plan = Plan.objects.create(name="Basic",price=49.99,stripe_price_id="price_test_123")
    subscription = Subscription.objects.create(user=user,plan=plan,stripe_customer_id="customer_test_123",status='pending',is_active=True)
    assert Subscription.objects.filter(id=subscription.id).exists()

@pytest.mark.django_db
def test_user_subscription(client,django_user_model):
    user = django_user_model.objects.create_user(username='test123',email="test@example.com", password="StrongPass123")
    plan = Plan.objects.create(name="Basic",price=49.99,stripe_price_id="price_test_123")
    Subscription.objects.create(user=user,plan=plan,stripe_customer_id="customer_test_123",status='pending',is_active=True)

    client = APIClient()
    client.force_authenticate(user=user) 
    
    url = reverse('user-subscription')
    response = client.get(url)
    assert response.status_code in [200]
    
