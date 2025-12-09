from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'setups', views.SetupViewSet)
router.register(r'reviews', views.ReviewViewSet)

urlpatterns = [
    # 1. Admin Panel
    path('admin/', admin.site.urls),

    # 2. API Endpoints (e.g., /api/setups/)
    path('api/', include(router.urls)),

    # 3. The New Frontend Gallery (Homepage)
    path('', views.home, name='home'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)