from django.core.exceptions import ValidationError


def validate_amount(amount):
    """Валидатор количества ингредиентов."""

    if amount < 1:
        raise ValidationError(
            'Количество ингредиента не может быть меньше одного.'
        )
    return amount
