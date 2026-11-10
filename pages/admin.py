
from django.contrib import admin
from .models import Category, Resource


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name",)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "resource_type",
        "category",
        "available",
        "created_at",
    )

    list_filter = ("available", "resource_type", "category")
    search_fields = ("title", "description")
    list_select_related = ("category",)
