"""
Test E2E for short links. Same scenario as in test_views.py,
but using live_server.
"""

import pytest
import requests
from unittest.mock import patch

from short import models as short_models


@pytest.mark.django_db
class TestToShortenViewE2E:

    def test_valid_data_succes(self, live_server):
        """Test valid data"""
        long_url = 'https://www.django-rest-framework.org/VeryLongUrl' * 25
        data = {'original_url': long_url}

        response = requests.post(
            f'{live_server}/api/short/to_shorten/',
            json=data
        )
        assert response.status_code == 201
        assert response.json()['short_url'] is not None

    def test_existing_short_link_success(self, live_server, short_base_url, short_link):
        
        data = {'original_url': short_link.original_url}
        response = requests.post(
            f'{live_server}/api/short/to_shorten/',
            json=data
        )
        assert response.status_code == 200
        assert response.json()['short_url'] == f'{live_server}/api/short/to_read/{short_link.code}'

    def test_post_then_get_success(self, live_server):
        """Test post then get success"""
        data = {'original_url': 'https://www.django-rest-framework.org/VeryLongUrl'}
        response = requests.post(
            f'{live_server.url}/api/short/to_shorten/',
            json=data
        )
        assert response.status_code == 201
        assert response.json()['short_url'] is not None

        code = response.json()['short_url'].split('/')[-1]

        assert len(code) == short_models.ShortLink.code.field.max_length
        response = requests.get(
            f'{live_server}/api/short/to_read/{code}'
        )

        assert response.status_code == 200
        assert response.json()['original_url'] == data['original_url']

    @patch('short.utils.create_short_url')
    def test_failed_to_create_short_link(self, mock_create_short_url, live_server):
        """Test failed to create short link"""
        mock_create_short_url.return_value = None, False
        data = {'original_url': 'https://www.django-rest-framework.org/VeryLongUrl'}
        response = requests.post(
            f'{live_server.url}/api/short/to_shorten/',
            json=data
        )
        assert response.status_code == 400
        assert response.json()['error'] == 'Failed to create short link, try again'

    def test_invalid_data(self, live_server):
        data = {'original_url': 'invalid_url'}
        response = requests.post(
            f'{live_server.url}/api/short/to_shorten/',
            json=data
        )
        assert response.status_code == 400
        assert response.json()['original_url'] == ['Enter a valid URL.']

    def test_no_data(self, live_server):
        response = requests.post(
            f'{live_server}/api/short/to_shorten/',
            json={}
        )
        assert response.status_code == 400
        assert response.json() == {'original_url': ['This field is required.']}

    def test_too_long_url(self, live_server):
        long_url = 'https://www.django-rest-framework.org/VeryLongUrl' * 50
        data = {'original_url': long_url}
        response = requests.post(
            f'{live_server.url}/api/short/to_shorten/',
            json=data
        )
        assert response.status_code == 400
        expected_error_array = [
            'Ensure this field has no more than 2000 characters.',
            'Enter a valid URL.',
        ]
        res_json = response.json()
        for error in expected_error_array:
            assert error in res_json['original_url']

    def test_invalid_method(self, live_server):
        data = {'original_url': 'https://www.django-rest-framework.org/VeryLongUrl'}
        response = requests.get(
            f'{live_server}/api/short/to_shorten/',
            json=data
        )
        assert response.status_code == 405


@pytest.mark.django_db
class TestToReadViewE2E:
    def test_valid_code(self, live_server, short_link):
        response = requests.get(
            f'{live_server.url}/api/short/to_read/{short_link.code}'
        )
        assert response.status_code == 200
        assert response.json()['original_url'] == short_link.original_url

    def test_invalid_code(self, live_server):
        response = requests.get(
            f'{live_server.url}/api/short/to_read/invalid_code'
        )
        assert response.status_code == 404

    def test_no_code(self, live_server):
        response = requests.get(
            f'{live_server.url}/api/short/to_read/'
        )
        assert response.status_code == 404

    def test_invalid_method(self, live_server):
        response = requests.post(
            f'{live_server.url}/api/short/to_read/123/')
        assert response.status_code == 405
