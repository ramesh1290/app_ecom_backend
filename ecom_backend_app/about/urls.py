from django.urls import path
from .views import AboutListCreateView, AboutDetailView

urlpatterns = [
    path("about/", AboutListCreateView.as_view(), name="about-list-create"),
    path("about/<int:pk>/", AboutDetailView.as_view(), name="about-detail"),
]