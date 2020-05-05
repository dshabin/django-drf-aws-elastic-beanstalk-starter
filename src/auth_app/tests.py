from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Profile
import json

class AuthTests(APITestCase):

    def test_auth(self):
        
        # Signup
        data = { 'username' : 'test@test.test' , 'password' : '123456' }
        url = reverse('auth-signup')
        response = self.client.post(url, data)
        res_data = json.loads(response.content)
        self.assertEqual(response.status_code, 201)


        # Login
        data = { 'username' : 'test@test.test' , 'password' : '123456' }
        url = reverse('auth-login')
        response = self.client.post(url, data)
        res_data = json.loads(response.content)
        token = res_data['data']['token']
        self.assertEqual(response.status_code, 200)


        
        # Fetch Current
        header = {
            'HTTP_AUTHORIZATION': 'Token ' + token,
        }
        url = reverse('auth-fetch-current')
        response = self.client.get(url, **header)
        res_data = json.loads(response.content)
        self.assertEqual(res_data['data']['user']['username'], 'test@test.test')
