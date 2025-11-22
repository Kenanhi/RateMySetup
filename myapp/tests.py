import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Setup

@pytest.mark.django_db
def test_user_registration():
    client = APIClient()
    data = {"email": "test@example.com", "password": "password123"}
    response = client.post('/api/users/', data)
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1

@pytest.mark.django_db
def test_create_setup():
    # Create user
    user = User.objects.create_user(email="dev@example.com", password="password")
    client = APIClient()
    client.force_authenticate(user=user)
    
    # Create setup
    data = {"title": "My Gaming Rig", "description": "RTX 4090 Beast"}
    response = client.post('/api/setups/', data)
    
    assert response.status_code == status.HTTP_201_CREATED
    assert Setup.objects.get().title == "My Gaming Rig"