from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from crm.models import Role, Profile


class RegistrationTests(APITestCase):
    def test_successful_registration(self):
        url = reverse('simple_register')
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Пользователь успешно зарегистрирован.')
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_registration_with_existing_username(self):
        url = reverse('simple_register')
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_registration_with_short_password(self):
        url = reverse('simple_register')
        data = {
            'username': 'newuser',
            'password': 'short'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_registration_with_missing_username(self):
        url = reverse('simple_register')
        data = {
            'password': 'validpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_registration_with_missing_password(self):
        url = reverse('simple_register')
        data = {
            'username': 'anotheruser'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)


class AuthenticationTests(APITestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword123'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_token_obtain_pair(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_refresh(self):
        url_obtain = reverse('token_obtain_pair')
        data = {
            'username': self.username,
            'password': self.password
        }
        response_obtain = self.client.post(url_obtain, data, format='json')
        refresh_token = response_obtain.data['refresh']

        url_refresh = reverse('token_refresh')
        response_refresh = self.client.post(url_refresh, {'refresh': refresh_token}, format='json')
        self.assertEqual(response_refresh.status_code, status.HTTP_200_OK)
        self.assertIn('access', response_refresh.data)

    def test_token_verify(self):
        url_obtain = reverse('token_obtain_pair')
        data = {
            'username': self.username,
            'password': self.password
        }
        response_obtain = self.client.post(url_obtain, data, format='json')
        access_token = response_obtain.data['access']

        url_verify = reverse('token_verify')
        response_verify = self.client.post(url_verify, {'token': access_token}, format='json')
        self.assertEqual(response_verify.status_code, status.HTTP_200_OK)


class ProtectedViewTests(APITestCase):
    def setUp(self):
        # Создаем пользователя и профиль
        self.username = 'testuser'
        self.password = 'testpassword123'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.profile = Profile.objects.create(author=self.user, surname='Иванов', name='Иван', course=1)

    def test_access_with_valid_role(self):
        role = Role.objects.create(name='Организатор')
        role.users.add(self.profile)

        url_obtain = reverse('token_obtain_pair')
        data = {
            'username': self.username,
            'password': self.password
        }
        response_obtain = self.client.post(url_obtain, data, format='json')
        access_token = response_obtain.data['access']

        url = reverse('protected_view')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Доступ разрешен!')

    def test_access_without_role(self):
        url_obtain = reverse('token_obtain_pair')
        data = {
            'username': self.username,
            'password': self.password
        }
        response_obtain = self.client.post(url_obtain, data, format='json')
        access_token = response_obtain.data['access']

        url = reverse('protected_view')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_access_for_unauthenticated_user(self):
        url = reverse('protected_view')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserViewTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123', email='user1@example.com')
        self.user2 = User.objects.create_user(username='user2', password='password123', email='user2@example.com')

        self.profile1 = Profile.objects.create(author=self.user1, surname='Иванов', name='Иван', course=1)
        self.profile2 = Profile.objects.create(author=self.user2, surname='Петров', name='Петр', course=2)

        self.role = Role.objects.create(name='Организатор')
        self.role.users.add(self.profile1)

        url_obtain = reverse('token_obtain_pair')
        response = self.client.post(url_obtain, {'username': 'user1', 'password': 'password123'}, format='json')
        self.access_token = response.data['access']

    def test_get_all_users(self):
        url = reverse('all_users')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        usernames = [user['username'] for user in response.data]
        self.assertIn(self.user1.username, usernames)
        self.assertIn(self.user2.username, usernames)

    def test_get_user_detail(self):
        url = reverse('user_detail', args=[self.user1.id])
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['username'], self.user1.username)
        self.assertEqual(response.data['email'], self.user1.email)

    def test_get_user_detail_not_found(self):
        url = reverse('user_detail', args=[999])
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)