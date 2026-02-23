from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"goal", views.GoalViewSet, basename="goal")
router.register(r"budget", views.BudgetViewSet, basename="budget")

urlpatterns = [
    path("", include(router.urls))
]