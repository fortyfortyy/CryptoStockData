from rest_framework import generics, permissions, status
from rest_framework.response import Response

from users.models import UserProfile
from users.serializers import RegisterSerializer


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