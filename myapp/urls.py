from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SetupViewSet, ReviewViewSet, UserViewSet, setup_detail

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'setups', SetupViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('setup/<int:pk>/', setup_detail, name='setup_detail'),
]