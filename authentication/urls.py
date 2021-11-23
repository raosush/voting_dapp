from django.urls import re_path, path
from rest_framework_simplejwt.views import TokenObtainPairView
from authentication.views import ProfileAPI, FetchProfile, TOTPCustomTokenRefreshView, UserAPI, RegisterAPI, TOTPCreateView, TOTPVerifyView

urlpatterns = [
   re_path(r'^totp/create$', TOTPCreateView.as_view(), name='totp-create'),
   re_path(r'^totp/login/(?P<token>[0-9]{6})$', TOTPVerifyView.as_view(), name='totp-login'),
   path('register', RegisterAPI.as_view()),
   path('user', UserAPI.as_view()),
   path('fetch_profile', FetchProfile.as_view(), name='fetch_profile'),
   path('profile', ProfileAPI.as_view(), name='profile'),
   path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('token/refresh', TOTPCustomTokenRefreshView.as_view(), name='token_refresh'),
]
