from django.contrib import admin
from .models import User

# Custom admin for User
class UserAdmin(admin.ModelAdmin):
    # Display in list view
    list_display = ('username', 'email', 'date_joined', 'is_active', 'image')
    list_filter = ('is_active', 'date_joined')  # Filters on the right
    search_fields = ('username', 'email')  # Search capability
    list_per_page = 25  # Pagination

    # Customizes form fields in detail view
    fieldsets = (
        ('Personal info', {'fields': ('username', 'email', 'password', 'image', 'role', 'country')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    filter_horizontal = ('groups', 'user_permissions')  # For many-to-many fields

    # Add custom actions if needed
    actions = ['activate_users', 'deactivate_users']

    # Example of a custom action to activate users
    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
    activate_users.short_description = "Activate selected users"

    # Example of a custom action to deactivate users
    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_users.short_description = "Deactivate selected users"

# Register the admin class with the associated model
admin.site.register(User, UserAdmin)
