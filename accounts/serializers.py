from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Public registration. Never allows setting staff/superuser/approval."""

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'},
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
    )

    class Meta:
        model = User
        fields = (
            'email', 'phone_number', 'first_name', 'last_name',
            'password', 'password_confirm', 'job_title',
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone_number': {'required': False},
        }

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(_('A user with this email already exists.'))
        return value.lower()

    def validate_phone_number(self, value):
        if value and User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(_('A user with this phone number already exists.'))
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': _('Passwords do not match.')})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        # Force safe defaults – never trust client for these
        user = User(
            **validated_data,
            is_active=True,
            is_staff=False,
            is_superuser=False,
            approval_status=User.ApprovalStatus.PENDING,
        )
        user.set_password(password)
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Login serializer.
    - Rejects inactive users (Django default).
    - Additionally rejects users who are not yet approved.
    """

    username_field = User.USERNAME_FIELD  # email

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if not user.is_active:
            raise serializers.ValidationError(
                _('This account is inactive.'),
                code='account_inactive',
            )

        if not user.is_approved:
            raise serializers.ValidationError(
                _('This account is pending approval or has been rejected. '
                  'Please contact the administrator.'),
                code='account_not_approved',
            )

        # Extra claims
        data['email'] = user.email
        data['full_name'] = user.get_full_name()
        data['approval_status'] = user.approval_status
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """Read / limited update of own profile. Role & approval are read-only."""

    full_name = serializers.CharField(source='get_full_name', read_only=True)
    groups = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name'
    )

    class Meta:
        model = User
        fields = (
            'id', 'email', 'phone_number', 'first_name', 'last_name',
            'full_name', 'avatar', 'date_of_birth', 'job_title',
            'branch', 'personnel_code', 'approval_status',
            'date_joined', 'last_login', 'groups', 'created_at', 'updated_at',
        )
        read_only_fields = (
            'id', 'email', 'approval_status', 'date_joined',
            'last_login', 'groups', 'created_at', 'updated_at',
            'personnel_code',  # only admin can change
        )


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True, write_only=True, validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(_('Old password is incorrect.'))
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(
                {'new_password_confirm': _('New passwords do not match.')}
            )
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save(update_fields=['password'])
        return user


class AdminUserSerializer(serializers.ModelSerializer):
    """Full user representation for administrators."""

    full_name = serializers.CharField(source='get_full_name', read_only=True)
    groups = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=__import__('django.contrib.auth.models', fromlist=['Group']).Group.objects.all(),
        required=False,
    )
    approved_by_email = serializers.EmailField(
        source='approved_by.email', read_only=True, allow_null=True
    )

    class Meta:
        model = User
        fields = (
            'id', 'email', 'phone_number', 'username',
            'first_name', 'last_name', 'full_name', 'avatar',
            'date_of_birth', 'personnel_code', 'job_title', 'branch',
            'manager', 'internal_notes',
            'is_active', 'is_staff', 'is_superuser',
            'approval_status', 'requested_at', 'approved_by',
            'approved_by_email', 'approved_at', 'rejection_reason',
            'groups', 'date_joined', 'last_login',
            'created_at', 'updated_at',
        )
        read_only_fields = (
            'id', 'requested_at', 'approved_at', 'date_joined',
            'last_login', 'created_at', 'updated_at',
        )


class ApproveRejectSerializer(serializers.Serializer):
    reason = serializers.CharField(
        required=False, allow_blank=True, max_length=1000
    )
