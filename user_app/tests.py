import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
@pytest.mark.django_db
def test_user_registration(client):
    url = reverse("register")  
    data = {"username":"test123","email": "test@example.com", "password": "StrongPass123", "password2": "StrongPass123"}
    response = client.post(url, data)
    print(response)
    assert response.status_code in [201]
    # assert "test@example.com" in response.content.decode()

@pytest.mark.django_db
def test_login(client, django_user_model):
    user = django_user_model.objects.create_user(username='test123',email="test@example.com", password="StrongPass123")
    url = reverse("login")  
    response = client.post(url, {"email": "test@example.com", "password": "StrongPass123"})
    assert response.status_code in [200]
    # assert "access" in response.json()

@pytest.mark.django_db
def test_logout(client,django_user_model):
    user = django_user_model.objects.create_user(username='test123',email="test@example.com", password="StrongPass123")
    client = APIClient()
    client.force_authenticate(user=user) 
    
    url = reverse('logout')
    response = client.post(url, {"refresh_token": "dummy"})
    assert response.status_code in [200]