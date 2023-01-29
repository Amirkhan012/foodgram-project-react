from djoser.serializers import (
    UserCreateSerializer as BaseUserRegistrationSerializer,
    UserSerializer
)
from drf_base64.fields import Base64ImageField
from rest_framework import serializers, validators


from foodgram.models import Recipe
from user.models import User, Subscribe


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    username = serializers.CharField(
        required=True,
        validators=[
            validators.UniqueValidator(
                queryset=User.objects.all()
            )
        ],
    )
    email = serializers.EmailField(
        required=True,
        validators=[
            validators.UniqueValidator(
                queryset=User.objects.all()
            )
        ],
    )
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "email",
                  "first_name", "last_name",
                  "password", "role")


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', "username", "email",
                  "first_name", "last_name",
                  "role")


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            'id', 'email', 'username', 'first_name',
            'last_name', 'is_subscribed',)

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Subscribe.objects.filter(user=self.context['request'].user,
                                        author=obj).exists()


class ShortRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для краткого отображения сведений о избранных рецептах.
    """
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ("id", "name", "image",
                  "cooking_time")


class SubscribeSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count',)

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit_recipes = request.query_params.get('recipes_limit')
        if limit_recipes is not None:
            recipes = Recipe.objects.filter(author=obj)[:(int(limit_recipes))]
        else:
            recipes = Recipe.objects.filter(author=obj)
        context = {'request': request}
        return ShortRecipeSerializer(recipes, many=True,
                                     context=context).data

    @staticmethod
    def get_recipes_count(obj):
        return Recipe.objects.filter(author=obj).count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Subscribe.objects.filter(user=self.context['request'].user,
                                        author=obj).exists()
