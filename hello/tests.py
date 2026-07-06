from django.test import TestCase
from django.urls import reverse


class HelloViewTests(TestCase):
    def test_hello_endpoint(self):
        response = self.client.get(reverse('hello'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Hello from Django + Jenkins i love you')

    def test_health_endpoint(self):
        response = self.client.get(reverse('health'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})
