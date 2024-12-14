from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html

class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'is_active', 
        'is_staff', 
        'date_joined',
        'last_login',
        'user_status'
    )

    search_fields = ('username', 'email', 'first_name', 'last_name')

    list_filter = (
        'is_active', 
        'is_staff', 
        'is_superuser', 
        'date_joined'
    )

    actions = [
        'activate_users', 
        'deactivate_users', 
        'make_staff', 
        'remove_staff_status'
    ]

    def user_status(self, obj):
        if obj.is_superuser:
            return format_html('<span style="color: red;">Super Admin</span>')
        elif obj.is_staff:
            return format_html('<span style="color: green;">Staff</span>')
        elif obj.is_active:
            return format_html('<span style="color: blue;">Active</span>')
        else:
            return format_html('<span style="color: gray;">Inactive</span>')
    user_status.short_description = 'Status'

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
    activate_users.short_description = "Activate selected users"

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_users.short_description = "Deactivate selected users"

    def make_staff(self, request, queryset):
        queryset.update(is_staff=True)
    make_staff.short_description = "Make selected users staff"


    def remove_staff_status(self, request, queryset):
        queryset.update(is_staff=False)
    remove_staff_status.short_description = "Remove staff status"


    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 
                'is_staff', 
                'is_superuser', 
                'groups', 
                'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    readonly_fields = ('last_login', 'date_joined')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


admin.site.site_header = 'Apple Tech User Administration'
admin.site.site_title = 'Apple Tech User Admin Portal'
admin.site.index_title = 'Welcome to Apple Tech User Management'