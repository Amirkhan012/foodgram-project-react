
def check_request_return_boolean(self, obj, model):
    """Проверяем, что запрос есть, юзер не аноним и возвращаем булевую"""

    request = self.context.get('request')
    if not request or request.user.is_anonymous:
        return False
    return model.objects.filter(recipe=obj, user=request.user).exists()
