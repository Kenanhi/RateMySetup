from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Setup, Review

# Register the custom User model
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'username', 'is_staff', 'is_active']
    ordering = ['email']

@admin.register(Setup)
class SetupAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'created_at']
    search_fields = ['title', 'description']
    list_filter = ['created_at']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['setup', 'author', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['comment']