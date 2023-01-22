from django.urls import include, path
from rest_framework import routers

from .views import (TagViewSet, IngredientViewSet,
                    RecipeViewSet)

app_name = 'foodgram'


router = routers.DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet, basename='recipe')


urlpatterns = [
    path('', include(router.urls)),
]
