from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('photo', 'bio', 'country', 'birth_date', 'gender', 'adult_content_permission')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('photo', 'bio', 'country', 'birth_date', 'gender', 'adult_content_permission')}),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']


admin.site.register(CustomUser, CustomUserAdmin)
