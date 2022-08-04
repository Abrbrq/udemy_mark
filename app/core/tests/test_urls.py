from django.test import TestCase, Client
from django.urls import reverse


class UrlTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_api_schema_url(self):
        url = reverse('api-schema')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_api_docs(self):
        url = reverse('api-docs')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
