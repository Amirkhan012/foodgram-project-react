from rest_framework import mixins, viewsets


class ListRetrieveCreateUpdateDestroyMixin(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):
    '''Кастомный миксин для Views'''

    pass


def check_request_return_boolean(self, obj, model):
    """Проверяем, что запрос есть, юзер не аноним и возвращаем булевую"""

    request = self.context.get('request')
    if not request or request.user.is_anonymous:
        return False
    return model.objects.filter(recipe=obj, user=request.user).exists()
