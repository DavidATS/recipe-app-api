from django.urls import include
from django.urls import path
from recipe import views
from rest_framework.routers import DefaultRouter  # Registers ulrs for actions


router = DefaultRouter()
router.register("tags", views.TagViewSet)
router.register("ingredients", views.IngredientViewSet)
router.register("recipes", views.RecipeViewSet)

app_name = "recipe"

urlpatterns = [path("", include(router.urls))]
