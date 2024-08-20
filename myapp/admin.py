from django.contrib import admin
from .models import User, Setup, Review, Device
# Register your models here.
@admin.register(Setup)

class SetupAdmin(admin.ModelAdmin):
    list_display = ['setup_name', 'user', 'is_verified', 'created_at', 'updated_at']
    search_fields = ['setup_name', 'user']
    list_filter = ['is_verified', 'created_at', 'updated_at']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'description', 'numstars', 'is_active', 'created_at', 'updated_at']
    search_fields = ['user', 'description']
    list_filter = ['is_active', 'created_at', 'updated_at']

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['user', 'device_name', 'device_description', 'created_at', 'updated_at']
    search_fields = ['user', 'device_name']
    list_filter = ['created_at', 'updated_at']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'is_active', 'is_staff', 'is_superuser', 'created_at', 'last_login']
    search_fields = ['email', 'username']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'created_at', 'last_login']



