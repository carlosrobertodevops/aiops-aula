from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'email@empresa.com',
        'autofocus': True,
    }))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))

    error_messages = {
        'invalid_login': 'Credenciais inválidas',
        'inactive': 'Conta desativada. Contate o administrador.',
    }

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            # Verificar se o usuário existe e está inativo antes de autenticar
            try:
                user = User.objects.get(email=email)
                if not user.is_active and user.check_password(password):
                    raise ValidationError(
                        self.error_messages['inactive'],
                        code='inactive',
                    )
            except User.DoesNotExist:
                pass

        return super().clean()


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'role']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'role']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }


class ResetPasswordForm(forms.Form):
    password = forms.CharField(label='Nova senha', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password
