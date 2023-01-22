from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from drf_base64.fields import Base64ImageField

from .validators import validate_amount
from foodgram.models import (
    Tag, Ingredient, Recipe, IngredientsInRecipe, Favorite, Cart)
from user.serializers import CustomUserSerializer
from user.models import User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientsInRecipe
        fields = ('id', 'amount',)


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    ingredients = IngredientInRecipeSerializer(
        source='ingredients_recipe',
        many=True,
        read_only=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ("ingredients", "tags", "image",
                  "author", "name", "text",
                  "cooking_time")

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError(
                {'ingredients': 'Нужен хотя бы один ингредиент для рецепта'}
            )
        ingredients_list = []
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(
                Ingredient, id=ingredient_item['id']
            )
            if ingredient in ingredients_list:
                raise serializers.ValidationError(
                    {'ingredients': 'Ингредиенты не должны повторяться'}
                )
            validate_amount(int(ingredient_item['amount']))
            ingredients_list.append(ingredient)
        tags = self.initial_data.get('tags')
        if not tags:
            raise serializers.ValidationError(
                {'tags': 'Нужен хотя бы один тэг для рецепта'}
            )
        tags_list = []
        for tag_item in tags:
            tag = get_object_or_404(Tag, id=tag_item)
            if tag in tags_list:
                raise serializers.ValidationError(
                    {'tags': 'Теги в рецепте не должны повторяться'}
                )
            tags_list.append(tag)

        data['author'] = self.context.get('request').user
        data['ingredients'] = ingredients
        data['tags'] = tags
        return data

    def create_ingredients(self, ingredients, recipe):
        """Создаем связку ингредиентов для рецепта"""
        for ingredient_item in ingredients:
            IngredientsInRecipe.objects.bulk_create(
                [IngredientsInRecipe(
                    ingredient_id=ingredient_item['id'],
                    recipe=recipe,
                    amount=ingredient_item['amount']
                )]
            )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        image = validated_data.pop('image')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(image=image, **validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        recipe.save()
        return recipe

    def update(self, recipe, validated_data):
        recipe.ingredients.clear()
        self.create_ingredients(validated_data.pop('ingredients'), recipe)
        tags = validated_data.pop('tags')
        recipe.tags.set(tags)
        return super().update(recipe, validated_data)


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(
        source='ingredients_set',
        many=True,
        read_only=True
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "tags", "author", "ingredients", "is_favorited",
            "is_in_shopping_cart", "name", "image", "text", "cooking_time",)

    def get_is_favorited(self, obj):
        """
        Проверка на наличие рецепта в избранном.
        """
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(recipe=obj,
                                       user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        """
        Проверка на наличие рецепта в списке покупок.
        """
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Cart.objects.filter(recipe=obj,
                                   user=request.user).exists()


class ShortRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для краткого отображения сведений о избранных рецептах.
    """
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ("id", "name", "image",
                  "cooking_time")


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка избранного.
    """
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, data):
        user = data['user']
        recipe_id = data['recipe'].id
        if Favorite.objects.filter(user=user,
                                   recipe__id=recipe_id).exists():
            raise ValidationError(
                'Рецепт уже в избранном!')
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShortRecipeSerializer(
            instance.recipe,
            context=context
        ).data


class ShoppingListSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        model = Cart
        fields = ('user', 'recipe')

    def validate(self, data):
        user = data['user']
        recipe_id = data['recipe'].id
        if Cart.objects.filter(user=user,
                               recipe__id=recipe_id).exists():
            raise ValidationError(
                'Рецепт уже добавлен в корзину!'
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShortRecipeSerializer(
            instance.recipe,
            context=context
        ).data
