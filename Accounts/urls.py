from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"accounts", views.AccountViewSet, basename = "accounts")
router.register(r"category", views.CategoryViewSet, basename="category")
router.register(r"transaction", views.TransactionViewSet, basename="transaction")
router.register(r"transfer", views.TransferViewSet, basename="transfer")
router.register(r"recurring-transaction", views.RecurringTransactionViewSet, basename="recurring-transaction")

urlpatterns = [
    path("", include(router.urls)),
    path("dashboard/summary/", views.DashboardSummaryView.as_view(), name="dashboard-summary"),
]