from django.urls import path
from .views import WhyChooseUsListCreateView, WhyChooseUsDetailView,reorder_why_choose_us

urlpatterns = [
    path('why-choose-us/', WhyChooseUsListCreateView.as_view(), name='why-choose-us-list'),
    path('why-choose-us/<int:pk>/', WhyChooseUsDetailView.as_view(), name='why-choose-us-detail'),
    path("why-choose-us/reorder/", reorder_why_choose_us,name='reorder-why-choose-us'),
]