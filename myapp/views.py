from rest_framework import viewsets, permissions
from .models import Setup, Review, User
from .serializers import SetupSerializer, ReviewSerializer, UserSerializer
from .azure_vision import analyze_hardware_tags
from django.shortcuts import render, get_object_or_404

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        if hasattr(obj, 'author'):
            return obj.author == request.user
        return False

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] 

class SetupViewSet(viewsets.ModelViewSet):
    queryset = Setup.objects.all()
    serializer_class = SetupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        image = self.request.FILES.get('image') or serializer.validated_data.get('image')
        hardware_tags = analyze_hardware_tags(image) if image else []
        serializer.save(owner=self.request.user, hardware_tags=hardware_tags)

    def perform_update(self, serializer):
        image = self.request.FILES.get('image') or serializer.validated_data.get('image')
        if image:
            hardware_tags = analyze_hardware_tags(image)
            serializer.save(hardware_tags=hardware_tags)
        else:
            serializer.save()

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

def home(request):
    """Serve the gallery frontend."""
    return render(request, 'myapp/home.html')


def setup_detail(request, pk):
    """Serve the detail page for a single setup."""
    setup = get_object_or_404(Setup, pk=pk)
    return render(request, 'myapp/setup_detail.html', {'setup': setup})       