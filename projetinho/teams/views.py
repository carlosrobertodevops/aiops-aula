from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from accounts.mixins import AdminRequiredMixin
from teams.forms import AddMemberForm, TeamForm
from teams.models import Team, TeamMembership

User = get_user_model()


class TeamListView(LoginRequiredMixin, ListView):
    template_name = 'teams/team_list.html'
    context_object_name = 'teams'

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Team.objects.all().order_by('name')
        return Team.objects.filter(memberships__user=user).distinct().order_by('name')


class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    template_name = 'teams/team_detail.html'
    context_object_name = 'team'

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Team.objects.all()
        return Team.objects.filter(memberships__user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['memberships'] = self.object.memberships.select_related('user').order_by('-is_manager', 'user__first_name')
        context['add_member_form'] = AddMemberForm()
        context['projects'] = self.object.projects.filter(status='active').order_by('name')
        return context


class TeamCreateView(AdminRequiredMixin, CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/team_form.html'

    def get_success_url(self):
        return reverse_lazy('teams:team_detail', args=[self.object.pk])

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Time "{self.object.name}" criado com sucesso.')
        return response


class TeamEditView(AdminRequiredMixin, UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/team_form.html'

    def get_success_url(self):
        return reverse_lazy('teams:team_detail', args=[self.object.pk])

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Time "{self.object.name}" atualizado com sucesso.')
        return response


class TeamDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        team = get_object_or_404(Team, pk=pk)
        name = team.name
        team.delete()
        messages.success(request, f'Time "{name}" excluído com sucesso.')
        return redirect('teams:team_list')


class TeamAddMemberView(AdminRequiredMixin, View):
    def post(self, request, pk):
        team = get_object_or_404(Team, pk=pk)
        form = AddMemberForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            is_manager = form.cleaned_data['is_manager']
            if TeamMembership.objects.filter(team=team, user=user).exists():
                messages.warning(request, f'{user.email} já é membro deste time.')
            else:
                TeamMembership.objects.create(team=team, user=user, is_manager=is_manager)
                messages.success(request, f'{user.email} adicionado ao time.')
        return redirect('teams:team_detail', pk=pk)


class TeamRemoveMemberView(AdminRequiredMixin, View):
    def post(self, request, pk, membership_pk):
        team = get_object_or_404(Team, pk=pk)
        membership = get_object_or_404(TeamMembership, pk=membership_pk, team=team)

        if membership.is_manager and team.memberships.filter(is_manager=True).count() == 1:
            messages.error(request, 'O time precisa ter pelo menos um gestor.')
            return redirect('teams:team_detail', pk=pk)

        membership.delete()
        messages.success(request, f'{membership.user.email} removido do time.')
        return redirect('teams:team_detail', pk=pk)


class TeamToggleManagerView(AdminRequiredMixin, View):
    def post(self, request, pk, membership_pk):
        team = get_object_or_404(Team, pk=pk)
        membership = get_object_or_404(TeamMembership, pk=membership_pk, team=team)

        if membership.is_manager and team.memberships.filter(is_manager=True).count() == 1:
            messages.error(request, 'O time precisa ter pelo menos um gestor.')
            return redirect('teams:team_detail', pk=pk)

        membership.is_manager = not membership.is_manager
        membership.save()
        action = 'promovido a gestor' if membership.is_manager else 'rebaixado a membro'
        messages.success(request, f'{membership.user.email} {action}.')
        return redirect('teams:team_detail', pk=pk)
