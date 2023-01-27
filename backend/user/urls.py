from django.urls import include, path
from djoser.views import TokenCreateView
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
    path('auth/token/login/',
         TokenCreateView.as_view(),
         name='login'),
    path('users/<int:pk>/subscribe/',
         follow_author,
         name='follow-author'),
    path('', include(router.urls))
]
