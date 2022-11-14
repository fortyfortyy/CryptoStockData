from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenViewBase, TokenRefreshView

from django.http import HttpResponseRedirect
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str

from users.utils import account_token
from users.utils import send_reset_password_email
from users.models import UserProfile
from users.serializers import CustomTokenObtainPairSerializer, ForgotPasswordSerializer, \
    ChangePasswordSerializer, RegisterSerializer, InActiveUser


class RegisterUserView(generics.CreateAPIView):
    """
    Create new user account
    """
    model = UserProfile
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    # def get(self, request, *args, **kwargs):
    #     return HttpResponseRedirect('/#/register')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'data': 'Account has been created.'}, status=status.HTTP_201_CREATED)


register_user_view = RegisterUserView.as_view()


class ForgotPasswordView(generics.ListAPIView):
    """
    Search user by given email, then send reset link
    """
    model = UserProfile
    serializer_class = ForgotPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect('/#/reset/password/')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            profile = self.model.objects.filter(email=email).first()

            if profile:
                send_reset_password_email(profile)

        return Response({
            'detail': 'If your email is associated with an account, '
                      'you should recieve an email shortly with the next steps'
        }, status=status.HTTP_200_OK, content_type='application/javascript')


forgot_password_view = ForgotPasswordView.as_view()


class SetPasswordView(generics.UpdateAPIView):
    """
    Checks if token and uidb64 is valid for a specific user, then set the new passwd
    """
    queryset = UserProfile
    token_generator = account_token
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(f"/#/account/set/password/{kwargs['uidb64']}/{kwargs['token']}/")

    def get_user(self, uidb64=None, queryset=None):
        if uidb64 is None or queryset is None:
            return None

        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = queryset.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, queryset.DoesNotExist):
            user = None

        return user

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        user = self.get_user(self.kwargs.get('uidb64', None), queryset)
        if user is not None:
            token = self.kwargs.get('token', None)
            if token and self.token_generator.check_token(user=user, token=token):
                return user

        user = None
        return user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if user is None:
            return Response({"invalid": "Invalid token or uidb"}, status=status.HTTP_400_BAD_REQUEST,
                            content_type='application/javascript')

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user.set_password(serializer.data.get('password'))
            user.save()
            return Response({"detail": "Password has been updated."}, status=status.HTTP_200_OK,
                            content_type='application/javascript')

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type='application/javascript')


set_password_view = SetPasswordView.as_view()


class ActivateAccountView(generics.UpdateAPIView):
    """
    Checks whether the link is valid for the given user.
    Then activate account.
    """
    queryset = UserProfile
    permission_classes = [permissions.AllowAny]

    # def get(self, request, *args, **kwargs):
    #     return HttpResponseRedirect(f"/#/account/activate/{kwargs['uidb64']}/{kwargs['token']}/")

    def update(self, request, *args, **kwargs):
        try:
            uid = smart_str(urlsafe_base64_decode(kwargs.get('uidb64', None)))
            profile = self.queryset.objects.filter(pk=uid).first()
        except (TypeError, ValueError, OverflowError, KeyError):
            profile = None

        if profile is not None and account_token.check_token(profile, kwargs.get('token', None)):
            profile.is_active = True
            profile.save()

            return Response({'account': 'Account has been activated!'}, status=status.HTTP_200_OK,
                            content_type='application/javascript')

        content = {'account': 'Account is already activated'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST, content_type='application/javascript')


activate_account_view = ActivateAccountView.as_view()


class CustomTokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    Returns HTTP 406 when user is inactive and HTTP 401 when login credentials are invalid.
    """
    serializer_class = CustomTokenObtainPairSerializer

    # def get(self, request, *args, **kwargs):
    #     return HttpResponseRedirect('/#/login')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed:
            raise InActiveUser()
        except TokenError:
            raise InvalidToken()

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


custom_token_obtain_view = CustomTokenObtainPairView.as_view()


class CustomTokenRefreshView(TokenRefreshView):
    """
    Refresh given old token with the new one
    method get() is not allowed.
    """

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect('/#/404')


custom_token_refresh_view = CustomTokenRefreshView.as_view()
