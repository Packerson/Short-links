from django.contrib import admin
from short import models as short_models


@admin.register(short_models.ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    list_display = ['code', 'original_url', 'date_created']
    search_fields = ['code', 'original_url']
    list_filter = ['date_created']
    readonly_fields = ['date_created']
