from django.urls import include, path
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from Accounts import urls as accounts_urls
from currencies import urls as currencies_urls
from CreditCard import urls as creditcard_urls
from UserAccount import urls as user_urls
from Goals import urls as goal_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("rest_framework.urls", namespace="rest_framework")), 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("acc/", include(accounts_urls)),
    path("currencies/", include(currencies_urls)),
    path("cards/", include(creditcard_urls)),
    path("user/", include(user_urls)),
    path("goal/", include(goal_urls)),
]
