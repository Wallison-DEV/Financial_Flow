from django.urls import include, path
from django.contrib import admin

from Accounts import urls as accounts_urls
from currencies import urls as currencies_urls
from CreditCard import urls as creditcard_urls
from UserAccount import urls as user_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("rest_framework.urls", namespace="rest_framework")), 
    path("acc/", include(accounts_urls)),
    path("currencies/", include(currencies_urls)),
    path("cards/", include(creditcard_urls)),
    path("user/", include(user_urls))
]
