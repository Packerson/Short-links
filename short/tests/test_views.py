import pytest
from django.conf import settings
from django.urls import reverse
from unittest.mock import patch

from short import models as short_models


@pytest.mark.django_db
class TestToShortenView:

    link_url = 'https://www.django-rest-framework.org/VeryLongUrl'

    def _create_post_request(self, api_client, data):
        return api_client.post(
            reverse('api:short:to_shorten'),
            data=data,
            format='json'
        )

    def test_valid_data_succes(self, api_client):
        """Test valid data"""
        long_url = self.link_url * 25
        data = {'original_url': long_url}

        response = self._create_post_request(api_client, data)
        assert response.status_code == 201
    
        short_url = response.data['short_url']
        code = short_url.split('/')[-1]
        assert len(code) == short_models.ShortLink.code.field.max_length

    def test_existing_short_link_success(self, api_client, short_link):
        """Test existing short link"""
        data = {'original_url': short_link.original_url}
        response = self._create_post_request(api_client, data)

        assert response.status_code == 200
        assert response.data['short_url'] == f'{settings.SHORT_BASE_URL}/{short_link.code}'

    def test_post_then_get_success(self, api_client, ):
        """Test post then get success"""
        data = {'original_url': self.link_url}

        # post
        response = self._create_post_request(api_client, data)

        short_link = short_models.ShortLink.objects.get(original_url=self.link_url)

        assert response.status_code == 201
        assert response.data['short_url'] == f'{settings.SHORT_BASE_URL}/{short_link.code}'

        # get code from short_url
        code = response.data['short_url'].split('/')[-1]
        assert len(code) == short_models.ShortLink.code.field.max_length

        # get
        response = api_client.get(
            reverse(
                'api:short:to_read',
                kwargs={'code': short_link.code}
            ),
            format='json'
        )
        assert response.status_code == 200
        assert response.data['original_url'] == self.link_url

    @patch('short.utils.create_short_url')
    def test_failed_to_create_short_link(self, mock_create_short_url, api_client):
        """Test failed to create short link"""
        mock_create_short_url.return_value = None, False
        data = {'original_url': 'https://www.django-rest-framework.org/VeryLongUrl'}
        response = self._create_post_request(api_client, data)

        assert response.status_code == 503
        assert response.data['error'] == 'Failed to create short link, try again'

    def test_invalid_data(self, api_client):
        """Test invalid data"""
        data = {'original_url': 'invalid_url'}
        response = self._create_post_request(api_client, data)

        assert response.status_code == 400
        assert response.data['original_url'] == ['Enter a valid URL.']

    def test_no_data(self, api_client):
        """Test no data"""
        response = self._create_post_request(api_client, {})

        assert response.status_code == 400
        assert response.data == {'original_url': ['This field is required.']}

    def test_too_long_url(self, api_client):
        """Test too long url"""
        long_url = 'https://www.django-rest-framework.org/VeryLongUrl' * 50
        data = {'original_url': long_url}

        response = self._create_post_request(api_client, data)

        assert response.status_code == 400

        expected_error_array = [
            f'Ensure this field has no more than {short_models.ShortLink.original_url.field.max_length} characters.',
            'Enter a valid URL.',
        ]
        res_json = response.json()
        for error in expected_error_array:
            assert error in res_json['original_url']

    def test_invalid_method(self, api_client):
        """Test invalid method"""
        data = {'original_url': 'https://www.django-rest-framework.org/VeryLongUrl'}
        response = api_client.get('/api/short/to_shorten/', data=data, format='json')
        assert response.status_code == 405


@pytest.mark.django_db
class TestToReadView:

    def _create_get_request(self, api_client, code):
        return api_client.get(
            reverse('api:short:to_read', kwargs={'code': code}),
            format='json'
        )

    def test_valid_code(self, api_client, short_link):
        """Test valid code"""
        response = self._create_get_request(api_client, short_link.code)
        assert response.status_code == 200
        assert response.data['original_url'] == short_link.original_url

    def test_invalid_code(self, api_client):
        """Test invalid code"""
        response = self._create_get_request(api_client, 'invalid_code')
        assert response.status_code == 404

    def test_no_code(self, api_client):
        """Test no code"""
        response = api_client.get('/api/short/to_read/', format='json')
        assert response.status_code == 404

    def test_invalid_method(self, api_client):
        """Test invalid method"""
        code = 'Ab12Cd'
        response = api_client.post(f'/api/short/to_read/{code}/', format='json')
        assert response.status_code == 405
