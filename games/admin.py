from django.contrib import admin
from .models import Category, Game


# Configuración para Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    list_filter = ("name",)


# Configuración para Game
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "release_date")
    list_filter = ("category", "release_date")
    search_fields = ("title", "description")
    date_hierarchy = "release_date"

    # Campos organizados en el formulario
    fieldsets = (
        ("Información Básica", {"fields": ("title", "category", "description")}),
        (
            "Requisitos del Sistema",
            {
                "fields": ("min_requirements", "max_requirements"),
                "classes": ("collapse",),
            },
        ),
        ("Multimedia", {"fields": ("cover_image", "trailer_url")}),
        ("Enlaces y Fecha", {"fields": ("download_link", "release_date")}),
    )
