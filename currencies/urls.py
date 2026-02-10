from django.urls import include, path
from rest_framework import routers

from . import views
route  = routers.DefaultRouter()
route.register(r"currency", views.CurrencyViewSet)

urlpatterns = [
    path("", include(route.urls)),
]