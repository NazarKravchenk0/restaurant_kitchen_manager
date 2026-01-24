from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from kitchen.models import Cook, Dish, DishType, Ingredient


@admin.register(Cook)
class CookAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Kitchen info", {"fields": ("years_of_experience",)}),
    )
    list_display = UserAdmin.list_display + ("years_of_experience",)
    search_fields = UserAdmin.search_fields + ("first_name", "last_name")


@admin.register(DishType)
class DishTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name",)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name",)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "dish_type", "price", "created_at")
    list_filter = ("dish_type",)
    search_fields = ("name", "description")
    filter_horizontal = ("cooks", "ingredients")
