from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'phone', 'is_email_verified', 'is_phone_verified', 'is_staff')
    list_filter = ('is_staff', 'is_email_verified', 'is_phone_verified')
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'password')}),
        ('Verification', {'fields': ('is_email_verified', 'is_phone_verified')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Dates', {'fields': ('last_login',)}),
        ('Groups', {'fields': ('groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password1', 'password2', 'is_staff', 'is_superuser')}
        ),
    )
    search_fields = ('email', 'phone')
    ordering = ('email',)

# Register the models with the admin site
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)




# Register your models here.
