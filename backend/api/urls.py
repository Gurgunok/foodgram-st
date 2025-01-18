from rest_framework.routers import DefaultRouter
from django.urls import path, include
from users.views import UserViewSet, LogoutView, CustomAuthToken
from recipes.views import RecipeViewSet, IngredientViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
router.register("recipes", RecipeViewSet, basename="recipe")
router.register("ingredients", IngredientViewSet, basename="ingredient")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/token/login/", CustomAuthToken.as_view(), name="token_login"),
    path("auth/token/logout/", LogoutView.as_view(), name="token_logout"),
]
