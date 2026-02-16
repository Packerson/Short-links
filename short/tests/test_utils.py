import pytest
from unittest.mock import patch
from django.db import IntegrityError

from short import models as short_models
from short import utils as short_utils


def test_generate_code():
    """Test _generate_code function"""
    assert len(short_utils._generate_code()) == short_utils.DEFAULT_CODE_LENGTH
    assert len(short_utils._generate_code()) == short_models.ShortLink.code.field.max_length
    assert isinstance(short_utils._generate_code(), str)


def test_validate_attempts():
    """Test _validate_attempts function"""
    assert short_utils._validate_attempts(1) == 1
    assert short_utils._validate_attempts(10) == 10
    assert short_utils._validate_attempts(11) == short_utils.MAX_ATTEMPTS
    assert short_utils._validate_attempts(0) == short_utils.MIN_ATTEMPTS
    assert short_utils._validate_attempts(-1) == short_utils.MIN_ATTEMPTS
    assert short_utils._validate_attempts("A") == short_utils.DEFAULT_ATTEMPTS
    assert short_utils._validate_attempts(None) == short_utils.DEFAULT_ATTEMPTS


@pytest.mark.django_db
class TestCreateShortUrl:
    # pytest short/tests/test_utils.py::TestCreateShortUrl::test_max_attempts -s

    @patch('short.models.ShortLink.objects.get_or_create')
    def test_max_attempts(self, mock_get_or_create, short_link):
        """Test max attempts"""
        mock_get_or_create.side_effect = [
            IntegrityError(),
            IntegrityError(),
            IntegrityError(),
        ]
        short_link, created = short_utils.create_short_url(
            original_url="https://www.django-rest-framework.org/VeryLongUrl",
            attempts=3
        )
        assert short_link is None
        assert created is False
        assert mock_get_or_create.call_count == 3


    @patch('short.models.ShortLink.objects.get_or_create')
    def test_exceeded_max_attempts(self, mock_get_or_create):
        """Test exceeded max attempts"""
        mock_get_or_create.side_effect = [
            IntegrityError(),
            IntegrityError(),
            IntegrityError(),
            IntegrityError(),
            IntegrityError(),
            IntegrityError(),
            IntegrityError(),
            IntegrityError(),
            IntegrityError(),
            IntegrityError(),
            IntegrityError(),
            IntegrityError(),
        ]
        short_link, created = short_utils.create_short_url(
            original_url="https://www.django-rest-framework.org/VeryLongUrl",
            attempts=11
        )
        assert short_link is None
        assert created is False
        assert mock_get_or_create.call_count == 10

    @patch('short.models.ShortLink.objects.get_or_create')
    def test_unexcpected_error_raised(self, mock_get_or_create):
        """Test unexcpected error raised"""
        mock_get_or_create.side_effect = Exception("Test exception")
        short_link, created = short_utils.create_short_url(
            original_url="https://www.django-rest-framework.org/VeryLongUrl",
            attempts=1
        )
        assert short_link is None
        assert created is False

    @patch('short.models.ShortLink.objects.get_or_create')
    def test_invalid_original_url(self, mock_get_or_create):
        """Test invalid original url"""
        short_link, created = short_utils.create_short_url(
            original_url=None,
            attempts=1
        )
        assert short_link is None
        assert created is False
        assert mock_get_or_create.call_count == 0

    def test_invalid_attempts_succes(self):
        """Test invalid attempts success"""
        short_link, created = short_utils.create_short_url(
            original_url="https://www.django-rest-framework.org/VeryLongUrl",
            attempts="A"
        )
        assert short_link is not None
        assert created is True

    def test_create_short_link_success(self):
        """Test create short link success"""
        short_link, created = short_utils.create_short_url(
            original_url="https://www.django-rest-framework.org/VeryLongUrl",
            attempts=1
        )
        assert short_link is not None
        assert created is True

    def test_get_existing_short_link(self, short_link):
        """Test get existing short link"""
        short_link_db, created = short_utils.create_short_url(
            original_url=short_link.original_url,
        )
        assert short_link is not None
        assert created is False
        assert short_link_db.id == short_link.id
