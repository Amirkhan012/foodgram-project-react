from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Subscribe, User
from .serializers import SubscribeSerializer


@api_view(['POST', 'DELETE'])
@permission_classes([permissions.IsAuthenticated, ])
def follow_author(request, pk):
    """
    Подписка на автора.
    """
    user = get_object_or_404(User, username=request.user.username)
    author = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        if user.id == author.id:
            content = {'errors': 'Нельзя подписаться на себя'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            Subscribe.objects.create(user=user, author=author)
        except IntegrityError:
            content = {'errors': 'Вы уже подписаны на данного автора'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        follows = User.objects.all().filter(username=author.username)
        serializer = SubscribeSerializer(
            follows,
            many=True,
            context={'request': request},
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == 'DELETE':
        try:
            subscription = Subscribe.objects.get(user=user, author=author)
        except ObjectDoesNotExist:
            content = {'errors': 'Вы не подписаны на данного автора'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        subscription.delete()
        return HttpResponse('Вы успешно отписаны от этого автора',
                            status=status.HTTP_204_NO_CONTENT)


class SubscriptionListView(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для генерации списка подписок пользователя.
    """
    queryset = User.objects.all()
    serializer_class = SubscribeSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (permissions.IsAuthenticated,)
    search_fields = ('^following__user',)

    def get_queryset(self):
        user = self.request.user
        new_queryset = User.objects.filter(following__user=user)
        return new_queryset
