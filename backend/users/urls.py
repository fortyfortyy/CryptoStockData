from django.urls import path

from rest_framework_simplejwt.views import (
    TokenVerifyView,
)

from users import views

urlpatterns = [
    path('token/', views.custom_token_obtain_view, name='token_obtain_pair'),   # to log in
    path('token/refresh/', views.custom_token_refresh_view, name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('register/', views.register_user_view, name='register'),
    path('activate/<uidb64>/<token>/',
         views.activate_account_view, name='activate_account'),

    path('password/reset/', views.forgot_password_view, name='forgot_password'),
    path('password/set/<uidb64>/<token>/', views.set_password_view, name='password_set_confirm'),
]
