from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from Ticket.models import Ticket

User = get_user_model()

class TicketCreationAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Strong-Password123', email='testuser@example.com')
        self.client.login(username='testuser', password='Strong-Password123')

    def test_ticket_creation_success(self):
        url = reverse('ticket-create')  # Make sure 'ticket-create' matches your URL configuration
        data = {
            'title': 'Test Ticket',
            'content': 'This is a test ticket.',
            'user_id': self.user.id,
        }
        response = self.client.post(url, data, format='json')

        # Print response data for debugging
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['status_code'], 201)
        self.assertEqual(response.data['message'], 'Ticket created successfully')
        self.assertEqual(response.data['ticket']['title'], 'Test Ticket')

        # Check if the ticket was created
        self.assertTrue(Ticket.objects.filter(title='Test Ticket').exists())

    def test_ticket_creation_failure(self):
        url = reverse('ticket-create')  # Make sure 'ticket-create' matches your URL configuration
        data = {
            'content': 'This is a test ticket without a title.',
            'user_id': self.user.id,
        }
        response = self.client.post(url, data, format='json')

        # Print response data for debugging
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertEqual(response.data['status_code'], 400)
        self.assertEqual(response.data['message'], 'Ticket creation failed')
        self.assertIn('title', response.data['errors'])

        # Check if the ticket was not created
        self.assertFalse(Ticket.objects.filter(description='This is a test ticket without a title.').exists())