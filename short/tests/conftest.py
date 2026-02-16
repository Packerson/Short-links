import pytest
from rest_framework.test import APIClient
from short import models as short_models


@pytest.fixture
def api_client():
    """Provide an API client for tests"""
    return APIClient()


@pytest.fixture
def short_base_url(settings, live_server):
    settings.SHORT_BASE_URL = f"{live_server.url}/api/short/to_read"
    return settings.SHORT_BASE_URL


@pytest.fixture
def short_link(db):
    """Create a short link"""
    return short_models.ShortLink.objects.create(
        original_url="https://www.django-rest-framework.org/VeryLongUrl/",
        code="Ab12Cd"
    )
