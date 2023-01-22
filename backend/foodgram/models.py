from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models

from user.models import User


class Tag(models.Model):
    name = models.CharField(
        'Имя тега',
        max_length=150,
        blank=False,
    )
    hexcolor = ColorField(
            format="hex",
            blank=False,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=False,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return (f'{self.name}({self.slug})')


class Ingredient(models.Model):
    name = models.CharField(
        'Имя ингридиента',
        max_length=150,
        blank=False,
    )
    measurement_unit = models.CharField(
        'Измерение ингридиента',
        max_length=30,
        blank=False,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsInRecipe',
        related_name='ingredientinrecipe',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='tags',
        verbose_name='Теги'
    )
    image = models.ImageField(
        verbose_name='Фото блюда',
        upload_to='recipes/',
        help_text='Загрузите изображение блюда',
    )
    name = models.CharField(
        'Имя рецепта',
        max_length=200,
        blank=False,
    )
    text = models.TextField(
        'Описание рецепта',
        blank=False,
    )
    cooking_time = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1)
        ],
        blank=False,
    )
    pub_date = models.DateTimeField(
        'Дата буликации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        """Список отсортирован по дате публикации."""
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        """Отображаются только первые 30 символов имени."""
        return self.name[:30]


class IngredientsInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='ingredientrecipe_set',
        on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        validators=[MinValueValidator(1)]
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_recipe'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_recipe_ingredient'
            )
        ]

    def __str__(self):
        return (f'''{self.recipe}: ингредиент-{self.ingredient} –
                    количество-{self.amount}''')


class Favorite(models.Model):
    """
    Модель избранных рецептов.
    recipe - рецепт
    user - пользователь, добавивший рецепт в избранное.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='in_favorite',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorite',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='unique_favorite',
            ),
        )

    def __str__(self):
        return f'Рецепт {self.recipe} в избранном пользователя {self.user}'


class Cart(models.Model):
    """
    Модель списка покупок.
    recipe - рецепт
    user - пользователь.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='cart_recipe'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='cart_user',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='cart_recipe_user_exists',
            ),
        )

    def __str__(self):
        return f'Рецепт {self.recipe} у пользователя {self.user}'