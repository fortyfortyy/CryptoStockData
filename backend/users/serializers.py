from rest_framework import serializers

from django.core import exceptions
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

from users.models import UserProfile


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for create user account.
    """
    password = serializers.CharField(write_only=True, max_length=128)
    password2 = serializers.CharField(write_only=True, max_length=128)

    class Meta:
        model = UserProfile
        fields = (
            'email',
            'password',
            'password2',
            'username',
        )

    def validate(self, data):
        """
        Check if the given passwords are the same.
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': _("Passwords are not the same.")})
        elif len(data['password']) > 128 or len(data['password2']) > 128:
            raise serializers.ValidationError("Passwords are too long")

        del data['password2']
        return data

    def validate_email(self, email):
        qs = UserProfile.objects.filter(email__iexact=email.lower())
        if qs.exists():
            raise serializers.ValidationError(f"User with this email already exists.'")

        return email.lower()

    def validate_username(self, username):
        return username.lower()

    def create(self, validated_data):
        user = UserProfile.objects.create_user(
            email=validated_data.get('email'),
            username=validated_data.get('username'),
            password=validated_data.get('password'),
        )
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    """
    Serializer for sending reset password link to given email.
    """
    email = serializers.EmailField(max_length=255, write_only=True, required=True)

    def validate_email(self, value):
        errors = dict()
        try:
            validate_email(value)
        except exceptions.ValidationError as e:
            errors['email'] = list(e.message)

        if errors:
            raise serializers.ValidationError(errors)

        return value


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    password = serializers.CharField(max_length=128, required=True)
    password2 = serializers.CharField(max_length=128, required=True)

    def validate(self, data):
        """
        Check if the given passwords are the same
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': _("Passwords are not the same.")})
        elif len(data['password']) > 128 or len(data['password2']) > 128:
            raise serializers.ValidationError("Passwords are too long")
        return data
