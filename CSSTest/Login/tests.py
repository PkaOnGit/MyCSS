from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.core import mail
from Login.models import Role

User = get_user_model()

# Registration testing

# class RegistrationAPITestCase(APITestCase):
#     def setUp(self):
#         # Create a role for testing
#         self.role = Role.objects.create(name='TestRole')

#     def test_registration_success(self):
#         url = reverse('register_user')
#         data = {
#             'username': 'testuser',
#             'password': 'Strong-Password123',
#             'email': 'testuserxd@yopmail.com',
#             'roles': [self.role.id]
#         }
#         response = self.client.post(url, data, format='json')

#         # Print response data for debugging
#         print(response.data)
        
#         # Check the status code
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
#         # Check the response data
#         self.assertEqual(response.data['status'], 'success')
#         self.assertEqual(response.data['status_code'], 201)
#         self.assertEqual(response.data['message'], 'User registration successful')
#         self.assertEqual(response.data['user']['username'], 'testuser')
        
#         # Check if the user was created
#         self.assertTrue(User.objects.filter(username='testuser').exists())
        
#         # Check if the email was sent
#         self.assertEqual(len(mail.outbox), 1)
#         self.assertIn('Welcome testuser! Your registration is successful.', mail.outbox[0].body)

#     def test_registration_failure(self):
#         url = reverse('register_user')
#         data = {
#             'username': 'testuser',
#             'password': 'weak',
#             'email': 'testuserxd@yopmail.com',
#             'roles': [self.role.id]
#         }
#         response = self.client.post(url, data, format='json')
        
#         # Print response data for debugging
#         print(response.data)
        
#         # Check the status code
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
#         # Check the response data
#         self.assertEqual(response.data['status'], 'error')
#         self.assertEqual(response.data['status_code'], 400)
#         self.assertEqual(response.data['message'], 'User registration unsuccessful')
        
#         # Update the error message check
#         self.assertIn('This password is too short. It must contain at least 8 characters.', response.data['errors']['password'])

#         # Check if the user was not created
#         self.assertFalse(User.objects.filter(username='testuser').exists())
# -----------------------------Login--------------

class LoginAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='StrongPassword123', email='testuser@example.com')

    def test_login_success(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'StrongPassword123'
        }
        response = self.client.post(url, data, format='json')

        # Print response data for debugging
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], 'testuser')

    def test_login_failure_missing_fields(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            # Missing password
        }
        response = self.client.post(url, data, format='json')

        # Print response data for debugging
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertEqual(response.data['message'], 'Login unsuccessful')