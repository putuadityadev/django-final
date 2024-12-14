from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import AppleTechNews

@admin.register(AppleTechNews)
class AppleTechNewsAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'display_author', 
        'display_image', 
        'created_at', 
        'updated_at', 
        'content_preview'
    )

    search_fields = ('title', 'content', 'author__username')

    list_filter = ('created_at', 'author')

    readonly_fields = ('created_at', 'updated_at', 'display_full_image')

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'content')
        }),
        ('Media', {
            'fields': ('image', 'display_full_image')
        }),
        ('Metadata', {
            'fields': ('author', 'created_at', 'updated_at')
        })
    )


    def display_author(self, obj):
        return obj.author.username
    display_author.short_description = 'Author'


    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px;" />',
                obj.image.url
            )
        return 'No Image'
    display_image.short_description = 'Image'


    def display_full_image(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="max-height: 300px; max-width: 300px;" />'
            )
        return 'No Image'
    display_full_image.short_description = 'Full Image'

    def content_preview(self, obj):
        return f"{obj.content[:100]}..." if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'

    actions = ['mark_as_featured']

    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
    mark_as_featured.short_description = "Mark selected news as featured"


admin.site.site_header = 'Apple Tech News Administration'
admin.site.site_title = 'Apple Tech News Admin Portal'
admin.site.index_title = 'Welcome to Apple Tech News Management'