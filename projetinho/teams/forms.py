from django import forms
from django.contrib.auth import get_user_model

from teams.models import Team

User = get_user_model()


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class AddMemberForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        label='Usuário',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    is_manager = forms.BooleanField(label='Gestor', required=False)
