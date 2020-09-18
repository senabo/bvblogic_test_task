from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .api.serializer import UpdateProfileSerializer
from .models import UserProfile

User = get_user_model()


class TestCreateProfile(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a user.
        self.test_user = User.objects.create_user("test", "test@gmail.com", "password")

        # URL for creating an account.
        self.create_url = reverse("accounts:create_user")

    def test_create_user(self):
        """Ensure we can crate a user"""
        data = {
            "username": "test1",
            "email": "test1@gmail.com",
            "password": "somepassword123",
            "profile": {
                "name": "My Name",
                "about": "about me",
            },
        }

        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            f"Expected response code 201, received {response.status_code} instead",
        )
        self.assertEqual(response.data["username"], data["username"])
        self.assertEqual(response.data["email"], data["email"])
        self.assertFalse("password" in response.data)

    def test_create_user_without_profile(self):
        """Ensure we can't create user without profile"""

        data = {
            "username": "test2",
            "email": "test2@gmail.com",
            "password": "somepassword2123",
        }

        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_without_username(self):
        """Ensure we can't create user without username"""

        data = {
            "username": "",
            "email": "test3@gmail.com",
            "password": "somepassword3123",
            "profile": {
                "name": "Name",
                "about": "about me",
            },
        }

        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data["username"]), 1)

    def test_create_user_without_email(self):
        """Ensure we can't create user without email"""

        data = {
            "username": "test4",
            "email": "",
            "password": "somepassword4123",
            "profile": {
                "name": "Name",
                "about": "about me",
            },
        }

        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data["email"]), 1)

    def test_create_user_without_password(self):
        """Ensure we can't create user without password"""
        data = {
            "username": "test5",
            "email": "test5@gmail.com",
            "password": "",
            "profile": {
                "name": "Name",
                "about": "about me",
            },
        }

        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data["password"]), 1)

    def test_create_user_with_existing_username(self):
        """Ensure we can't create user with existing username"""

        data = {
            "username": "test",
            "email": "test5@gmail.com",
            "password": "somepassword5123",
            "profile": {
                "name": "Name",
                "about": "about me",
            },
        }

        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data["username"]), 1)

    def test_create_user_with_existing_email(self):
        """Ensure we can't create user with existing email"""

        data = {
            "username": "test6",
            "email": "test@gmail.com",
            "password": "somepassword6123",
            "profile": {
                "name": "Name",
                "about": "about me",
            },
        }

        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data["email"]), 1)


class TestUpdateProfile(APITestCase):
    def setUp(self):
        self.username = "test"
        self.password = "password"

        self.another_username = "another"

        # Create users in db
        self.test_user = User.objects.create_user(
            self.username,
            "test@gmail.com",
            self.password,
        )
        self.another_user = User.objects.create_user(
            self.another_username,
            "t@gmail.com",
            self.password,
        )

        # Create users profile in db
        UserProfile.objects.create(user=self.test_user)
        UserProfile.objects.create(user=self.another_user)

        # URL for updating a profile
        self.update_url = reverse(
            "accounts:update_user_profile", kwargs={"username": self.username}
        )

        # Create client with authentication
        self.auth_client = APIClient()
        self.client_is_authorized = self.auth_client.login(
            username=self.username,
            password=self.password,
        )

    def test_get_profile(self):
        """Ensure we can get profile"""

        serializer = UpdateProfileSerializer(self.test_user)
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_profile_without_authentication(self):
        """Ensure we can't update profile when we aren't authenticated"""

        data = {
            "current_password": "",
            "new_password": "",
            "email": "new_email@gmail.com",
            "profile": {"name": "New name", "about": "New about"},
        }
        response = self.client.put(self.update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_own_profile(self):
        """Ensure we can update own user and profile when we are authenticated"""

        data = {
            "username": self.username,
            "current_password": "",
            "new_password": "",
            "email": "new_email@gmail.com",
            "profile": {"name": "New name", "about": "New about"},
        }

        self.assertTrue(self.client_is_authorized, "Error. Client isn't authorized")

        response = self.auth_client.put(self.update_url, data, format="json")
        user = User.objects.get(username=self.username)
        serializer = UpdateProfileSerializer(user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_not_own_profile(self):
        """Ensure we can't update not own profile"""

        data = {
            "username": self.another_username,
            "current_password": "",
            "new_password": "",
            "email": "new_email@gmail.com",
            "profile": {"name": "New name", "about": "New about"},
        }

        self.assertTrue(self.client_is_authorized, "Error. Client isn't authorized")

        update_url = reverse(
            "accounts:update_user_profile", kwargs={"username": self.another_username}
        )

        response = self.auth_client.put(update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_password(self):
        """Ensure we can update our password"""

        self.assertTrue(self.client_is_authorized, "Error. Client isn't authorized")

        data = {
            "username": self.username,
            "current_password": self.password,
            "new_password": "newpassword123",
        }
        response = self.auth_client.patch(self.update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
