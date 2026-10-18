from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class AccountsAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('accounts:register')
        self.login_url = reverse('accounts:login')
        self.profile_url = reverse('accounts:profile')
        self.change_password_url = reverse('accounts:change_password')
        self.users_url = reverse('accounts:user-list')
        self.pending_url = reverse('accounts:user-pending')

        # Create groups
        self.admin_group = Group.objects.create(name='Admin')
        self.manager_group = Group.objects.create(name='Manager')

        # Superuser / Admin
        self.admin = User.objects.create_superuser(
            email='admin@emtiaz.local',
            password='AdminPass123!',
            first_name='Admin',
            last_name='User',
        )
        self.admin.groups.add(self.admin_group)

        # Approved regular user
        self.approved_user = User.objects.create_user(
            email='approved@emtiaz.local',
            password='UserPass123!',
            first_name='Approved',
            last_name='User',
            approval_status=User.ApprovalStatus.APPROVED,
        )

        # Pending user
        self.pending_user = User.objects.create_user(
            email='pending@emtiaz.local',
            password='UserPass123!',
            first_name='Pending',
            last_name='User',
            approval_status=User.ApprovalStatus.PENDING,
        )

        # Inactive user
        self.inactive_user = User.objects.create_user(
            email='inactive@emtiaz.local',
            password='UserPass123!',
            first_name='Inactive',
            last_name='User',
            approval_status=User.ApprovalStatus.APPROVED,
            is_active=False,
        )

    def _get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def test_register_success(self):
        data = {
            'email': 'newuser@emtiaz.local',
            'phone_number': '09121111111',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'StrongPass123!',
            'password_confirm': 'StrongPass123!',
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email='newuser@emtiaz.local')
        self.assertEqual(user.approval_status, User.ApprovalStatus.PENDING)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_register_cannot_set_staff(self):
        data = {
            'email': 'hacker@emtiaz.local',
            'first_name': 'Hack',
            'last_name': 'Er',
            'password': 'StrongPass123!',
            'password_confirm': 'StrongPass123!',
            'is_staff': True,
            'is_superuser': True,
            'approval_status': 'approved',
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email='hacker@emtiaz.local')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.approval_status, User.ApprovalStatus.PENDING)

    def test_login_approved_user(self):
        data = {'email': 'approved@emtiaz.local', 'password': 'UserPass123!'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_pending_user_rejected(self):
        data = {'email': 'pending@emtiaz.local', 'password': 'UserPass123!'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_inactive_user_rejected(self):
        data = {'email': 'inactive@emtiaz.local', 'password': 'UserPass123!'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertIn(response.status_code, (status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED))

    def test_pending_user_cannot_access_profile_with_token(self):
        """Even if a token somehow exists, IsApproved blocks access."""
        tokens = self._get_tokens(self.pending_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_approved_user_can_access_profile(self):
        tokens = self._get_tokens(self.approved_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'approved@emtiaz.local')

    def test_user_cannot_elevate_own_role_via_profile(self):
        tokens = self._get_tokens(self.approved_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        response = self.client.patch(
            self.profile_url,
            {'is_staff': True, 'approval_status': 'approved', 'job_title': 'Hacker'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.approved_user.refresh_from_db()
        self.assertFalse(self.approved_user.is_staff)
        self.assertEqual(self.approved_user.job_title, 'Hacker')

    def test_admin_can_list_pending(self):
        tokens = self._get_tokens(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        response = self.client.get(self.pending_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        emails = [u['email'] for u in response.data.get('results', response.data)]
        self.assertIn('pending@emtiaz.local', emails)

    def test_admin_can_approve_user(self):
        tokens = self._get_tokens(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        url = reverse('accounts:user-approve', kwargs={'pk': self.pending_user.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pending_user.refresh_from_db()
        self.assertEqual(self.pending_user.approval_status, User.ApprovalStatus.APPROVED)
        self.assertEqual(self.pending_user.approved_by, self.admin)

    def test_regular_user_cannot_approve(self):
        tokens = self._get_tokens(self.approved_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        url = reverse('accounts:user-approve', kwargs={'pk': self.pending_user.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_change_password(self):
        tokens = self._get_tokens(self.approved_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        data = {
            'old_password': 'UserPass123!',
            'new_password': 'NewStrongPass456!',
            'new_password_confirm': 'NewStrongPass456!',
        }
        response = self.client.post(self.change_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.approved_user.refresh_from_db()
        self.assertTrue(self.approved_user.check_password('NewStrongPass456!'))

    def test_deactivate_blocks_subsequent_access(self):
        tokens = self._get_tokens(self.approved_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
        # First access OK
        self.assertEqual(self.client.get(self.profile_url).status_code, status.HTTP_200_OK)

        # Admin deactivates
        self.approved_user.is_active = False
        self.approved_user.save()

        # Subsequent request with same token must fail
        response = self.client.get(self.profile_url)
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
