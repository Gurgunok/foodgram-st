from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

# Константы длины полей:
NAME_MAX_LENGTH = 200
UNIT_MAX_LENGTH = 50

User = get_user_model()


class Ingredient(models.Model):
    """
    Модель ингредиента.
    """
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name="Название",
    )
    measurement_unit = models.CharField(
        max_length=UNIT_MAX_LENGTH,
        verbose_name="Единица измерения",
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        # Сортировка по имени (по алфавиту)
        ordering = ["name"]
        # Уникальность пары (name, measurement_unit)
        constraints = [
            models.UniqueConstraint(
                fields=["name", "measurement_unit"],
                name="unique_ingredient_name_unit"
            )
        ]

    def __str__(self):
        # Отображаем и название, и ед. измерения
        return f"{self.name} ({self.measurement_unit})"


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор",
    )
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name="Название",
    )
    image = models.ImageField(
        upload_to="recipes/images/",
        verbose_name="Изображение",
    )
    text = models.TextField(verbose_name="Описание")
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        related_name="recipes",
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name="Время приготовления (мин)",
        validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ["name"]

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """
    Промежуточная модель для связи рецепта с ингредиентами и их количеством.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингредиент",
    )
    amount = models.PositiveIntegerField(
        verbose_name="Количество",
        validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = "Ингредиент рецепта"
        verbose_name_plural = "Ингредиенты рецепта"
        ordering = ["recipe", "ingredient"]
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_recipe_ingredient"
            )
        ]

    def __str__(self):
        return f"{self.recipe.name} — {self.ingredient.name} [{self.amount}]"


# ----- Вариант через абстрактную модель -----
class UserRecipeRelation(models.Model):
    """
    Абстрактная модель "Связь пользователь <-> рецепт".
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
    )

    class Meta:
        abstract = True
        ordering = ["user"]
        # Уникальность пары (user, recipe)
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique_user_recipe"
            )
        ]

    def __str__(self):
        return f"{self.user} -> {self.recipe}"


class Favorite(UserRecipeRelation):
    """
    "Избранное", наследуемся от абстрактной UserRecipeRelation.
    """
    class Meta(UserRecipeRelation.Meta):
        # Нужно переопределить, т.к. Meta не копируется полностью
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        ordering = ["user"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique_user_recipe_in_favorite"
            )
        ]


class ShoppingCart(UserRecipeRelation):
    """
    "Список покупок", также наследуемся от абстрактной UserRecipeRelation.
    """
    class Meta(UserRecipeRelation.Meta):
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
        ordering = ["user"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique_user_recipe_in_shopping_cart"
            )
        ]
