from django.urls import path

from teams import views

app_name = 'teams'

urlpatterns = [
    path('', views.TeamListView.as_view(), name='team_list'),
    path('novo/', views.TeamCreateView.as_view(), name='team_create'),
    path('<int:pk>/', views.TeamDetailView.as_view(), name='team_detail'),
    path('<int:pk>/editar/', views.TeamEditView.as_view(), name='team_edit'),
    path('<int:pk>/excluir/', views.TeamDeleteView.as_view(), name='team_delete'),
    path('<int:pk>/membros/adicionar/', views.TeamAddMemberView.as_view(), name='team_add_member'),
    path('<int:pk>/membros/<int:membership_pk>/remover/', views.TeamRemoveMemberView.as_view(), name='team_remove_member'),
    path('<int:pk>/membros/<int:membership_pk>/toggle-gestor/', views.TeamToggleManagerView.as_view(), name='team_toggle_manager'),
]
