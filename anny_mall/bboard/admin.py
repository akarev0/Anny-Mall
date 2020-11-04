from django.contrib import admin

from .models import Item, Rubric


class BbAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "price", "published")
    list_display_links = ("name", "description")
    search_fields = ("name", "published")


admin.site.register(Item, BbAdmin)
admin.site.register(Rubric)
