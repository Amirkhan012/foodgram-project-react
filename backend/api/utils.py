from django.db.models import F, Sum

from foodgram.models import IngredientsInRecipe


def get_list_ingredients(user):
    """
    Получение суммы ингредиентов из рецептов.
    """

    ingredients = IngredientsInRecipe.objects.filter(
        recipe__cart_recipe__user=user).values(
        name=F('ingredient__name'),
        measurement_unit=F('ingredient__measurement_unit')
    ).annotate(amount_ingredient=Sum('amount')).values_list(
        'ingredient__name', 'amount', 'ingredient__measurement_unit'
    )
    return ingredients
