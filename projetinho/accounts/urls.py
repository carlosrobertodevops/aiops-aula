from django.urls import path

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('usuarios/', views.UserListView.as_view(), name='user_list'),
    path('usuarios/novo/', views.UserCreateView.as_view(), name='user_create'),
    path('usuarios/<int:pk>/editar/', views.UserEditView.as_view(), name='user_edit'),
    path('usuarios/<int:pk>/toggle-active/', views.UserToggleActiveView.as_view(), name='user_toggle_active'),
    path('usuarios/<int:pk>/reset-senha/', views.UserResetPasswordView.as_view(), name='user_reset_password'),
]
