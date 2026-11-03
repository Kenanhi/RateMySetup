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
    setup = Setup.objects.get()
    assert setup.title == "My Gaming Rig"
    assert setup.hardware_tags == []
    assert response.data['hardware_tags'] == []


TINY_GIF = (
    b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00'
    b'!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
)


from django.test import override_settings

TEST_STORAGE_SETTINGS = {
    'DEFAULT_FILE_STORAGE': 'django.core.files.storage.FileSystemStorage',
    'STORAGES': {
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
    }
}


def test_azure_storage_configuration():
    """Verify that settings.py configures Azure Blob Storage as the default file storage."""
    from django.conf import settings
    assert settings.DEFAULT_FILE_STORAGE == 'storages.backends.azure_storage.AzureStorage'
    assert 'storages' in settings.INSTALLED_APPS


def test_security_settings():
    """Verify that ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS contain Azure VM IP."""
    from django.conf import settings
    assert '74.241.133.70' in settings.ALLOWED_HOSTS
    assert 'http://74.241.133.70' in settings.CSRF_TRUSTED_ORIGINS


@pytest.mark.django_db
@override_settings(**TEST_STORAGE_SETTINGS)
def test_azure_vision_graceful_degradation_when_keys_missing(monkeypatch):
    """Ensure upload succeeds with empty tags when Azure credentials are missing."""
    monkeypatch.delenv("AZURE_VISION_ENDPOINT", raising=False)
    monkeypatch.delenv("AZURE_VISION_KEY", raising=False)
    monkeypatch.delenv("AZURE_COMPUTER_VISION_ENDPOINT", raising=False)
    monkeypatch.delenv("AZURE_COMPUTER_VISION_KEY", raising=False)

    from django.core.files.uploadedfile import SimpleUploadedFile
    user = User.objects.create_user(email="vision_test@example.com", password="password")
    client = APIClient()
    client.force_authenticate(user=user)

    fake_image = SimpleUploadedFile("setup.gif", TINY_GIF, content_type="image/gif")
    data = {
        "title": "Minimalist Desk",
        "description": "Clean desk setup",
        "image": fake_image,
    }
    response = client.post('/api/setups/', data, format='multipart')

    assert response.status_code == status.HTTP_201_CREATED
    setup = Setup.objects.get(title="Minimalist Desk")
    assert setup.hardware_tags == []
    assert response.data["hardware_tags"] == []


@pytest.mark.django_db
@override_settings(**TEST_STORAGE_SETTINGS)
def test_azure_vision_graceful_degradation_on_api_error(monkeypatch):
    """Ensure upload succeeds with empty tags if Azure Computer Vision throws an error."""
    monkeypatch.setenv("AZURE_VISION_ENDPOINT", "https://mock.cognitiveservices.azure.com/")
    monkeypatch.setenv("AZURE_VISION_KEY", "mock_key")

    from django.core.files.uploadedfile import SimpleUploadedFile
    from unittest.mock import patch

    user = User.objects.create_user(email="vision_err@example.com", password="password")
    client = APIClient()
    client.force_authenticate(user=user)

    with patch("azure.ai.vision.imageanalysis.ImageAnalysisClient.analyze", side_effect=Exception("Azure API down")):
        fake_image = SimpleUploadedFile("setup_err.gif", TINY_GIF, content_type="image/gif")
        data = {
            "title": "Battlestation",
            "description": "RGB lighting",
            "image": fake_image,
        }
        response = client.post('/api/setups/', data, format='multipart')

    assert response.status_code == status.HTTP_201_CREATED
    setup = Setup.objects.get(title="Battlestation")
    assert setup.hardware_tags == []
    assert response.data["hardware_tags"] == []


@pytest.mark.django_db
@override_settings(**TEST_STORAGE_SETTINGS)
def test_azure_vision_success_tagging(monkeypatch):
    """Ensure detected tags from Azure Computer Vision are saved to hardware_tags."""
    monkeypatch.setenv("AZURE_VISION_ENDPOINT", "https://mock.cognitiveservices.azure.com/")
    monkeypatch.setenv("AZURE_VISION_KEY", "mock_key")

    from django.core.files.uploadedfile import SimpleUploadedFile
    from unittest.mock import patch, MagicMock

    user = User.objects.create_user(email="vision_ok@example.com", password="password")
    client = APIClient()
    client.force_authenticate(user=user)

    mock_result = MagicMock()
    tag1 = MagicMock()
    tag1.name = "monitor"
    tag2 = MagicMock()
    tag2.name = "mechanical keyboard"
    mock_result.tags.list = [tag1, tag2]

    with patch("azure.ai.vision.imageanalysis.ImageAnalysisClient.analyze", return_value=mock_result):
        fake_image = SimpleUploadedFile("setup_ok.gif", TINY_GIF, content_type="image/gif")
        data = {
            "title": "Dual Screen Setup",
            "description": "Ultrawide monitors and mechanical keyboard",
            "image": fake_image,
        }
        response = client.post('/api/setups/', data, format='multipart')

    assert response.status_code == status.HTTP_201_CREATED
    setup = Setup.objects.get(title="Dual Screen Setup")
    assert setup.hardware_tags == ["monitor", "mechanical keyboard"]
    assert response.data["hardware_tags"] == ["monitor", "mechanical keyboard"]