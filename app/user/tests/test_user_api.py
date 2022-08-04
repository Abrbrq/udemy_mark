"""
Tests for the user API
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUsrApiTests(TestCase):
    """Test the public features of the user API"""

    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'email': 'test@example.com',
            'password': 'test_pass123',
            'name': 'AnonymousUser'
        }

    def test_create_user_success(self):
        res = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=self.payload['email'])

        self.assertTrue(user.check_password(self.payload['password']))
        self.assertNotIn('password', res.data)

    def test_with_email_exists_error(self):
        create_user(**self.payload)
        res = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def password_too_short_error(self):
        res = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=self.payload.get('email')
        ).exists()

        self.assertFalse(user_exists)
