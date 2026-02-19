from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"credit-card", views.CreditCardViewSet, basename="credit-card")
router.register(r"invoices", views.InvoiceViewSet, basename="invoices")

urlpatterns = [
    path("", include(router.urls))
]