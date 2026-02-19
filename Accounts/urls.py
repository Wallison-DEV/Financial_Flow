from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"accounts", views.AccountViewSet, basename = "accounts")
router.register(r"category", views.CategoryViewSet, basename="category")
router.register(r"transaction", views.TransactionViewSet, basename="transaction")
router.register(r"transfer", views.TransferViewSet, basename="transfer")

urlpatterns = [
    path("", include(router.urls)),
]