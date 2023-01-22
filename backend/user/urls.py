from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SubscriptionListView, follow_author

app_name = 'user'

router = DefaultRouter()
router.register(
    r'users/subscriptions',
    SubscriptionListView,
    basename='subscriptions',
)

urlpatterns = [
    path('users/<int:pk>/subscribe/',
         follow_author,
         name='follow-author'),
    path('', include(router.urls))
]
