from django.http import HttpResponse
from django.template.loader import render_to_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from weasyprint import HTML

from .filters import IngredientFilter, RecipeFilter
from .mixins import ListRetrieveCreateUpdateDestroyMixin
from .permissions import (IsAdminOwnerOrReadOnly,
                          IsAdminOrReadOnly)
from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeSerializer,
                          ShortRecipeSerializer)
from .utils import get_list_ingredients
from foodgram.models import Tag, Ingredient, Recipe


class TagViewSet(ListRetrieveCreateUpdateDestroyMixin):
    """Класс для Tag объектов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(ListRetrieveCreateUpdateDestroyMixin):
    """Класс для Ingredient объектов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(ListRetrieveCreateUpdateDestroyMixin):
    """Класс для Recipe объектов."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAdminOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return RecipeCreateSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def _favorite_shopping_post_delete(self, related_manager):
        recipe = self.get_object()
        if self.request.method == 'DELETE':
            related_manager.get(recipe_id=recipe.id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if related_manager.filter(recipe=recipe).exists():
            return Response(
                'Рецепт уже в избранном',
                status=status.HTTP_204_NO_CONTENT)
        related_manager.create(recipe=recipe)
        serializer = ShortRecipeSerializer(instance=recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True,
            permission_classes=[permissions.IsAuthenticated],
            methods=['POST', 'DELETE'], )
    def favorite(self, request, pk=None):
        return self._favorite_shopping_post_delete(
            request.user.favorite)

    @action(detail=True,
            permission_classes=[permissions.IsAuthenticated],
            methods=['POST', 'DELETE'], )
    def shopping_cart(self, request, pk=None):
        return self._favorite_shopping_post_delete(
            request.user.cart_user)

    @action(detail=False)
    def download_shopping_cart(self, request):
        ingredients = get_list_ingredients(request.user)
        html_template = render_to_string('pdf_template.html',
                                         {'ingredients': ingredients})
        html = HTML(string=html_template)
        result = html.write_pdf()
        response = HttpResponse(result, content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; filename=cart_list.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        return response
