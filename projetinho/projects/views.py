from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from projects.forms import ProjectForm
from projects.models import Project
from teams.models import Team, TeamMembership


class ProjectPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Permite acesso se admin ou gestor do time do projeto."""

    def get_team(self):
        if hasattr(self, "object") and self.object:
            return self.object.team
        team_pk = self.kwargs.get("team_pk")
        if team_pk:
            return get_object_or_404(Team, pk=team_pk)
        return None

    def test_func(self):
        user = self.request.user
        if user.is_admin:
            return True
        team = self.get_team()
        if team:
            return TeamMembership.objects.filter(
                team=team, user=user, is_manager=True
            ).exists()
        return False


class ProjectVisibilityMixin(LoginRequiredMixin):
    """Filtra projetos visíveis para o usuário."""

    def get_visible_teams(self):
        user = self.request.user
        if user.is_admin:
            return Team.objects.all()
        return Team.objects.filter(memberships__user=user)


class ProjectCreateView(ProjectPermissionMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_form.html"

    def get_team(self):
        return get_object_or_404(Team, pk=self.kwargs["team_pk"])

    def form_valid(self, form):
        form.instance.team = self.get_team()
        response = super().form_valid(form)
        messages.success(
            self.request, f'Projeto "{self.object.name}" criado com sucesso.'
        )
        return response

    def get_success_url(self):
        return reverse_lazy("projects:project_detail", args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team"] = self.get_team()
        return context


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "projects/project_detail.html"
    context_object_name = "project"

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Project.objects.all()
        visible_teams = Team.objects.filter(memberships__user=user)
        return Project.objects.filter(team__in=visible_teams)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["can_manage"] = (
            user.is_admin
            or TeamMembership.objects.filter(
                team=self.object.team, user=user, is_manager=True
            ).exists()
        )
        return context


class ProjectEditView(ProjectPermissionMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_form.html"

    def get_team(self):
        return self.get_object().team

    def get_success_url(self):
        return reverse_lazy("projects:project_detail", args=[self.object.pk])

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, f'Projeto "{self.object.name}" atualizado com sucesso.'
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team"] = self.object.team
        return context


class ProjectArchiveView(ProjectPermissionMixin, View):
    def get_team(self):
        project = get_object_or_404(Project, pk=self.kwargs["pk"])
        return project.team

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if project.status == Project.STATUS_ACTIVE:
            project.status = Project.STATUS_ARCHIVED
            project.save()
            messages.success(request, f'Projeto "{project.name}" arquivado.')
        else:
            project.status = Project.STATUS_ACTIVE
            project.save()
            messages.success(request, f'Projeto "{project.name}" reativado.')
        return redirect("projects:project_detail", pk=pk)


class ProjectListByTeamView(LoginRequiredMixin, ListView):
    template_name = "projects/project_list.html"
    context_object_name = "projects"

    def get_team(self):
        team = get_object_or_404(Team, pk=self.kwargs["team_pk"])
        user = self.request.user
        if not user.is_admin:
            if not TeamMembership.objects.filter(team=team, user=user).exists():
                return None
        return team

    def dispatch(self, request, *args, **kwargs):
        self.team = self.get_team()
        if self.team is None:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = Project.objects.filter(team=self.team)
        show_archived = self.request.GET.get("archived") == "1"
        if not show_archived:
            qs = qs.filter(status=Project.STATUS_ACTIVE)
        return qs.order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team"] = self.team
        context["show_archived"] = self.request.GET.get("archived") == "1"
        return context
