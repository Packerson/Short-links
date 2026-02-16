import pytest
from rest_framework.test import APIClient
from short import models as short_models


@pytest.fixture
def api_client():
    """Provide an API client for tests"""
    return APIClient()


@pytest.fixture
def short_link(db):
    """Create a short link"""
    return short_models.ShortLink.objects.create(
        original_url="https://www.django-rest-framework.org/VeryLongUrl",
        code="Ab12Cd"
    )
