from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from accounts.forms import (
    EmailAuthenticationForm,
    ResetPasswordForm,
    UserCreateForm,
    UserEditForm,
)
from accounts.mixins import AdminRequiredMixin

User = get_user_model()


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True


class CustomLogoutView(LoginRequiredMixin, View):
    def post(self, request):
        logout(request)
        return redirect('accounts:login')


class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    ordering = ['first_name', 'last_name']


class UserCreateView(AdminRequiredMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Usuário {self.object.email} criado com sucesso.')
        return response


class UserEditView(AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Usuário {self.object.email} atualizado com sucesso.')
        return response


class UserToggleActiveView(AdminRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        if user.is_active:
            # Desativando — verificar se é o último admin
            if user.is_admin and User.objects.filter(role=User.ROLE_ADMIN, is_active=True).count() == 1:
                messages.error(request, 'Não é possível desativar o último administrador.')
                return redirect('accounts:user_list')
            user.is_active = False
            user.save()
            messages.success(request, f'Usuário {user.email} desativado.')
        else:
            user.is_active = True
            user.save()
            messages.success(request, f'Usuário {user.email} reativado.')

        return redirect('accounts:user_list')


class UserResetPasswordView(AdminRequiredMixin, View):
    template_name = 'accounts/reset_password.html'

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = ResetPasswordForm()
        return request.META.get('_render', self._render)(request, user, form)

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, f'Senha de {user.email} redefinida com sucesso.')
            return redirect('accounts:user_list')
        return self._render(request, user, form)

    def _render(self, request, user, form):
        from django.shortcuts import render
        return render(request, self.template_name, {'form': form, 'target_user': user})
