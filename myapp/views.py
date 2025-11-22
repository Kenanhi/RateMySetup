from rest_framework import viewsets, permissions
from .models import Setup, Review, User
from .serializers import SetupSerializer, ReviewSerializer, UserSerializer

# Custom permission: Only owners can edit/delete their content
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Check if the object has an 'owner' attribute (Setup) or 'author' (Review)
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        if hasattr(obj, 'author'):
            return obj.author == request.user
        return False

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # This line is CRITICAL: it allows anyone (even strangers) to register
    permission_classes = [permissions.AllowAny] 

class SetupViewSet(viewsets.ModelViewSet):
    queryset = Setup.objects.all()
    serializer_class = SetupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)