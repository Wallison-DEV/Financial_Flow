from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet, basename="user")
router.register(r"profile", views.ProfileViewSet, basename="profile")

urlpatterns= [
    path("", include(router.urls))
]