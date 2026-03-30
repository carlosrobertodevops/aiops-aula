from django.urls import path

from projects import views

app_name = 'projects'

urlpatterns = [
    path('time/<int:team_pk>/', views.ProjectListByTeamView.as_view(), name='project_list_by_team'),
    path('time/<int:team_pk>/novo/', views.ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('<int:pk>/editar/', views.ProjectEditView.as_view(), name='project_edit'),
    path('<int:pk>/arquivar/', views.ProjectArchiveView.as_view(), name='project_archive'),
]
