from django.contrib import admin

from .models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
)


class RecipeIngredientInline(admin.TabularInline):
    """
    TabularInline позволяет редактировать связанные
    RecipeIngredient прямо внутри рецепта.
    """
    model = RecipeIngredient
    extra = 1   # При создании рецепта будет 1 пустая строка под ингредиент
    min_num = 1    # Требовать минимум 1 ингредиент


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """
    Админ-модель для Ingredient.
    """
    list_display = ("id", "name", "measurement_unit")
    search_fields = ("name",)
    ordering = ("name",)  # По умолчанию сортируем по названию


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Админ-модель для Recipe.
    """
    list_display = ("id", "name", "author", "cooking_time", "favorites_count")
    list_filter = ("author", "name", "ingredients")  # Фильтры справа
    search_fields = ("name", "author__username")  # Поле поиска
    inlines = [RecipeIngredientInline]  # Вставляем связь с ингредиентами

    # Пример группировки полей в админке через fieldsets
    fieldsets = (
        (None, {
            "fields": (
                "name", "author", "image",
                "text", "cooking_time"
            )
        }),
    )

    # Считаем, сколько раз рецепт добавлен в избранное
    def favorites_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()
    favorites_count.short_description = "Добавлено в избранное"


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    """
    Если хотите отдельно видеть RecipeIngredient в админке,
    помимо inlines.
    """
    list_display = ("id", "recipe", "ingredient", "amount")
    search_fields = ("recipe__name", "ingredient__name")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """
    Админ-модель для Favorite (Избранное).
    """
    list_display = ("id", "user", "recipe")
    search_fields = ("user__username", "recipe__name")


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """
    Админ-модель для ShoppingCart.
    """
    list_display = ("id", "user", "recipe")
    search_fields = ("user__username", "recipe__name")
