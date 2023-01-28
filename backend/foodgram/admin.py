from django.contrib import admin

from api.forms import TagForm
from .models import (
        Tag, Ingredient, Recipe, IngredientsInRecipe,
        Favorite, Cart)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    ordering = ('id',)
    search_fields = ('name',)
    form = TagForm


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit', 'get_in_recipes_count',)
    search_fields = ('name',)
    ordering = ('measurement_unit',)

    def get_in_recipes_count(self, obj):
        return IngredientsInRecipe.objects.filter(ingredient=obj.id).count()


class RecipeIngredientInline(admin.TabularInline):
    model = IngredientsInRecipe
    min_num = 1
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline, )
    list_display = ('id', 'name', 'author', 'text',)
    list_filter = ('name', 'author', 'tags',)
    readonly_fields = ('in_favorite',)

    def in_favorite(self, obj):
        return obj.in_favorite.all().count()


@admin.register(Favorite)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)


@admin.register(Cart)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
