from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from crm.models import Role, Profile, Skill


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


class SkillTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='password123', email='user1@example.com')
        self.profile = Profile.objects.create(author=self.user, surname='Иванов', name='Иван', course=1)
        self.role = Role.objects.create(name='Организатор')
        self.role.users.add(self.profile)

        self.skill1 = Skill.objects.create(name='Skill 1')
        self.skill2 = Skill.objects.create(name='Skill 2')
        self.skill3 = Skill.objects.create(name='Skill 3')

        url_obtain = reverse('token_obtain_pair')
        response = self.client.post(url_obtain, {'username': 'user1', 'password': 'password123'}, format='json')
        self.access_token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        self.url = reverse('get_all_skills')
        self.skill_url1 = reverse('get_skill_by_id', args=[self.skill1.pk])
        self.skill_url2 = reverse('get_skill_by_id', args=[self.skill2.pk])
        self.skill_url3 = reverse('get_skill_by_id', args=[self.skill3.pk])
        self.add_skill_url = reverse('add_skill')
        self.delete_skill_url = reverse('delete_skill', args=[self.skill1.pk])  # Удаление первого навыка

    def test_get_all_skills(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Проверяем, что три навыка возвращаются

    def test_get_skill_by_id(self):
        response = self.client.get(self.skill_url1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.skill1.name)

    def test_get_skill_by_invalid_id(self):
        response = self.client.get(reverse('get_skill_by_id', args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Навык не найден.')

    def test_add_skill(self):
        data = {'name': 'New Skill'}
        response = self.client.post(self.add_skill_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Skill.objects.count(), 4)

    def test_add_skill_invalid(self):
        data = {'name': ''}
        response = self.client.post(self.add_skill_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_skill(self):
        response = self.client.delete(self.delete_skill_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Skill.objects.count(), 2)

    def test_delete_skill_invalid(self):
        response = self.client.delete(reverse('delete_skill', args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Навык не найден.')