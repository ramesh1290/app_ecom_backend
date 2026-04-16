from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("products.urls")),
    path("api/", include("user.urls")),
    path("api/", include("contacts.urls")),
    path("api/", include("carts.urls")),
    path("api/", include("whychooseus.urls")),
    path("api/", include("about.urls")),
    path("api/dashboard/", include("dashboard.urls")),
    path("api/payments/", include("payments.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)