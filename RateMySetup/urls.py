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
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),

    path('', views.home, name='home'),
    path('setup/<int:pk>/', views.setup_detail, name='setup_detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)