
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'fullname', 'created', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'fullname')
    ordering = ('created',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'fullname')}),
        ('Permissions', {'fields': ('is_staff',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fullname' ,'password1', 'password2'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(BaseUserManager, CustomUserManager)