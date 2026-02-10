from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"accounts", views.AccountViewSet)
router.register(r"category", views.CategoryViewSet)
router.register(r"transaction", views.TransactionViewSet)
router.register(r"transfer", views.TransferViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework"))
]