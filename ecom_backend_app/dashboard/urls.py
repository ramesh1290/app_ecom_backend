from django.urls import path
from .views import DashboardCategoryListCreateView, DashboardCategoryRetrieveUpdateDestroyView, DashboardContactDeleteView, DashboardContactListView, DashboardProductListCreateView, DashboardProductRetrieveUpdateDeleteView, DashboardSummaryView

urlpatterns = [
    path("summary/", DashboardSummaryView.as_view(), name="dashboard-summary"),
     path("products/", DashboardProductListCreateView.as_view(), name="dashboard-products"),
    path("products/<int:pk>/", DashboardProductRetrieveUpdateDeleteView.as_view(), name="dashboard-product-detail"),
     path("categories/", DashboardCategoryListCreateView.as_view(), name="dashboard-categories"),
    path("categories/<int:pk>/", DashboardCategoryRetrieveUpdateDestroyView.as_view(), name="dashboard-category-detail"),
     path("contacts/", DashboardContactListView.as_view(), name="dashboard-contacts"),
    path("contacts/<int:pk>/", DashboardContactDeleteView.as_view(), name="dashboard-contact-delete"),
]