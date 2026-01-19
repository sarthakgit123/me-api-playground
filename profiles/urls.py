from django.urls import path
from .views import (
    HealthView,
    ProfileView,
    ProjectCreateView,
    ProjectSearchView,
)

urlpatterns = [
    path("health/", HealthView.as_view()),
    path("profile/", ProfileView.as_view()),
    path("projects/", ProjectCreateView.as_view()),
    path("projects/search/", ProjectSearchView.as_view()),
]
