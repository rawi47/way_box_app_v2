from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
import requests

class TestConectionStatus(APITestCase):
    def setUp(self):
        self.url = reverse('connection_status')

    def test_anonymous(self):
        """Anonymous user can get status"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class TestCatchAll(APITestCase):
    def setUp(self):
        self.url = reverse("catch_all",kwargs={'path':"miaw"})

    def test_anonymous(self):
        """Anonymous user can get status"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_anonymous_establichement_name(self):
    #     """Anonymous user should get no result"""
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
