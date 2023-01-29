from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/', include('user.urls')),
    path('api/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path(
        'api/docs/redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
