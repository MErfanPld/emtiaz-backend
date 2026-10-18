from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .permissions import IsApproved, IsAdminUser, IsAdminOrManager, IsSelfOrAdmin
from .serializers import (
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
    AdminUserSerializer,
    ApproveRejectSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """Public registration endpoint. Creates a pending account."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                'detail': 'Registration successful. Your account is pending administrator approval.',
                'email': user.email,
                'approval_status': user.approval_status,
            },
            status=status.HTTP_201_CREATED,
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    """Login – only approved & active users receive tokens."""

    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


class LogoutView(APIView):
    """Blacklist the refresh token."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {'detail': 'Refresh token is required.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {'detail': 'Invalid or expired token.'},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProfileView(generics.RetrieveUpdateAPIView):
    """Current user profile (GET / PATCH)."""

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsApproved]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    """Change own password."""

    permission_classes = [IsAuthenticated, IsApproved]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Password changed successfully.'})


class UserViewSet(viewsets.ModelViewSet):
    """
    Admin / Manager management of users.
    - list / retrieve: AdminOrManager
    - update / partial_update / destroy: Admin only
    - custom actions: approve, reject, activate, deactivate
    """

    queryset = User.objects.all().select_related('approved_by', 'manager').prefetch_related('groups')
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, IsApproved, IsAdminOrManager]
    http_method_names = ['get', 'patch', 'post', 'head', 'options']

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy', 'set_groups'):
            return [IsAuthenticated(), IsApproved(), IsAdminUser()]
        return super().get_permissions()

    def get_queryset(self):
        qs = super().get_queryset()
        status_filter = self.request.query_params.get('approval_status')
        if status_filter:
            qs = qs.filter(approval_status=status_filter)
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() in ('true', '1'))
        return qs

    @action(detail=False, methods=['get'], url_path='pending')
    def pending(self, request):
        """List accounts waiting for approval."""
        qs = self.get_queryset().filter(approval_status=User.ApprovalStatus.PENDING)
        page = self.paginate_queryset(qs)
        serializer = self.get_serializer(page or qs, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsApproved, IsAdminUser])
    def approve(self, request, pk=None):
        user = self.get_object()
        if user.approval_status == User.ApprovalStatus.APPROVED:
            return Response(
                {'detail': 'User is already approved.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.approve(by_user=request.user)
        return Response(
            {
                'detail': 'User approved successfully.',
                'approval_status': user.approval_status,
                'approved_at': user.approved_at,
            }
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsApproved, IsAdminUser])
    def reject(self, request, pk=None):
        user = self.get_object()
        serializer = ApproveRejectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if user.approval_status == User.ApprovalStatus.REJECTED:
            return Response(
                {'detail': 'User is already rejected.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.reject(
            by_user=request.user,
            reason=serializer.validated_data.get('reason', ''),
        )
        return Response(
            {
                'detail': 'User rejected.',
                'approval_status': user.approval_status,
                'rejection_reason': user.rejection_reason,
            }
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsApproved, IsAdminUser])
    def activate(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save(update_fields=['is_active', 'updated_at'])
        return Response({'detail': 'User activated.', 'is_active': True})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsApproved, IsAdminUser])
    def deactivate(self, request, pk=None):
        user = self.get_object()
        if user == request.user:
            return Response(
                {'detail': 'You cannot deactivate your own account.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.is_active = False
        user.save(update_fields=['is_active', 'updated_at'])
        return Response({'detail': 'User deactivated.', 'is_active': False})
