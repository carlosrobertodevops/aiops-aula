from django.conf import settings
from django.db import models


class Team(models.Model):
    name = models.CharField('nome', max_length=100, unique=True)
    description = models.TextField('descrição', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'time'
        verbose_name_plural = 'times'
        ordering = ['name']

    def __str__(self):
        return self.name


class TeamMembership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='team_memberships')
    is_manager = models.BooleanField('é gestor', default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'membro do time'
        verbose_name_plural = 'membros do time'
        unique_together = ['team', 'user']

    def __str__(self):
        role = 'Gestor' if self.is_manager else 'Membro'
        return f'{self.user.email} - {self.team.name} ({role})'
