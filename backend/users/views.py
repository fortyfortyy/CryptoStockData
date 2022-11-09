from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
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


class ActivateAccountView(APIView):
    """
    Checks whether the link is valid for the given user.
    Then activate account.
    """
    model = UserProfile
    renderer_classes = [JSONRenderer]

    # def get(self, request, *args, **kwargs):
    #     return HttpResponseRedirect(f"/#/account/activate/{kwargs['uidb64']}/{kwargs['token']}/")

    def post(self, request, *args, **kwargs):
        try:
            uid = smart_str(urlsafe_base64_decode(kwargs.get('uidb64', None)))
            profile = self.model.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, KeyError, self.model.DoesNotExist):
            profile = None

        if profile is not None and account_token.check_token(profile, kwargs.get('token', None)):
            profile.is_active = True
            profile.save()

            return Response({'account': 'Account has been activated!'}, status=status.HTTP_200_OK,
                            content_type='application/javascript')

        content = {'account': 'Link is invalid or account is already activated'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST, content_type='application/javascript')


activate_account_view = ActivateAccountView.as_view()


class CustomTokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    Returns HTTP 406 when user is inactive and HTTP 401 when login credentials are invalid.
    """
    serializer_class = CustomTokenObtainPairSerializer

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect('/#/login')

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
