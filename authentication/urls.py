from django.urls import re_path, path
from authentication.views import ProfileAPI, TOTPCustomTokenRefreshView, UserAPI, RegisterAPI, TOTPCreateView, TOTPVerifyView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [
   re_path(r'^totp/create$', TOTPCreateView.as_view(), name='totp-create'),
   re_path(r'^totp/login/(?P<token>[0-9]{6})$', TOTPVerifyView.as_view(), name='totp-login'),
   path('register', RegisterAPI.as_view()),
   path('user', UserAPI.as_view()),
   path('profile', ProfileAPI.as_view(), name='fetch_profile'),
   path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('token/refresh', TOTPCustomTokenRefreshView.as_view(), name='token_refresh'),
]
