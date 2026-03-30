from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('accounts:login')),
    path('accounts/', include('accounts.urls')),
    path('times/', include('teams.urls')),
    path('projetos/', include('projects.urls')),
]
