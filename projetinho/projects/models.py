from django.db import models

from teams.models import Team


class Project(models.Model):
    STATUS_ACTIVE = 'active'
    STATUS_ARCHIVED = 'archived'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Ativo'),
        (STATUS_ARCHIVED, 'Arquivado'),
    ]

    name = models.CharField('nome', max_length=200)
    description = models.TextField('descrição', blank=True)
    status = models.CharField('status', max_length=10, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='projects', verbose_name='time')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'projeto'
        verbose_name_plural = 'projetos'
        ordering = ['name']

    def __str__(self):
        return self.name
