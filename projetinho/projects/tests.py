from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from projects.models import Project
from teams.models import Team, TeamMembership

User = get_user_model()


class ProjectModelTests(TestCase):
    def test_create_project(self):
        team = Team.objects.create(name="Backend")
        project = Project.objects.create(name="API v2", team=team)
        self.assertEqual(str(project), "API v2")
        self.assertEqual(project.status, Project.STATUS_ACTIVE)
        self.assertEqual(project.team, team)

    def test_project_belongs_to_team(self):
        team = Team.objects.create(name="Backend")
        project = Project.objects.create(name="API", team=team)
        self.assertIn(project, team.projects.all())


class ProjectPermissionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(
            email="admin@e.com", password="Admin123", role=User.ROLE_ADMIN
        )
        self.manager = User.objects.create_user(
            email="gestor@e.com", password="Gestor123", role=User.ROLE_MANAGER
        )
        self.member = User.objects.create_user(
            email="membro@e.com", password="Membro123", role=User.ROLE_MEMBER
        )
        self.team = Team.objects.create(name="Backend")
        TeamMembership.objects.create(
            team=self.team, user=self.manager, is_manager=True
        )
        TeamMembership.objects.create(
            team=self.team, user=self.member, is_manager=False
        )

    def test_admin_can_create_project(self):
        self.client.login(email="admin@e.com", password="Admin123")
        response = self.client.post(
            reverse("projects:project_create", args=[self.team.pk]),
            {"name": "New Project", "description": ""},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Project.objects.filter(name="New Project").exists())

    def test_manager_can_create_project_in_their_team(self):
        self.client.login(email="gestor@e.com", password="Gestor123")
        response = self.client.post(
            reverse("projects:project_create", args=[self.team.pk]),
            {"name": "Manager Project", "description": ""},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Project.objects.filter(name="Manager Project").exists())

    def test_member_cannot_create_project(self):
        self.client.login(email="membro@e.com", password="Membro123")
        response = self.client.post(
            reverse("projects:project_create", args=[self.team.pk]),
            {"name": "Hacked", "description": ""},
        )
        self.assertEqual(response.status_code, 403)

    def test_manager_cannot_create_project_in_other_team(self):
        other_team = Team.objects.create(name="Frontend")
        self.client.login(email="gestor@e.com", password="Gestor123")
        response = self.client.post(
            reverse("projects:project_create", args=[other_team.pk]),
            {"name": "Hacked", "description": ""},
        )
        self.assertEqual(response.status_code, 403)

    def test_manager_can_edit_project(self):
        project = Project.objects.create(name="Old", team=self.team)
        self.client.login(email="gestor@e.com", password="Gestor123")
        response = self.client.post(
            reverse("projects:project_edit", args=[project.pk]),
            {"name": "Updated", "description": ""},
        )
        self.assertEqual(response.status_code, 302)
        project.refresh_from_db()
        self.assertEqual(project.name, "Updated")

    def test_manager_can_archive_project(self):
        project = Project.objects.create(name="ToArchive", team=self.team)
        self.client.login(email="gestor@e.com", password="Gestor123")
        response = self.client.post(
            reverse("projects:project_archive", args=[project.pk])
        )
        project.refresh_from_db()
        self.assertEqual(project.status, Project.STATUS_ARCHIVED)


class ProjectVisibilityTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(
            email="admin@e.com", password="Admin123", role=User.ROLE_ADMIN
        )
        self.member = User.objects.create_user(
            email="membro@e.com", password="Membro123", role=User.ROLE_MEMBER
        )
        self.team_a = Team.objects.create(name="Team A")
        self.team_b = Team.objects.create(name="Team B")
        TeamMembership.objects.create(
            team=self.team_a, user=self.member, is_manager=False
        )
        self.project_a = Project.objects.create(name="Project A", team=self.team_a)
        self.project_b = Project.objects.create(name="Project B", team=self.team_b)
        self.outsider = User.objects.create_user(
            email="outsider@e.com", password="Outsider123", role=User.ROLE_MEMBER
        )

    def test_member_can_see_project_in_their_team(self):
        self.client.login(email="membro@e.com", password="Membro123")
        response = self.client.get(
            reverse("projects:project_detail", args=[self.project_a.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_member_cannot_see_project_in_other_team(self):
        self.client.login(email="membro@e.com", password="Membro123")
        response = self.client.get(
            reverse("projects:project_detail", args=[self.project_b.pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_admin_can_see_any_project(self):
        self.client.login(email="admin@e.com", password="Admin123")
        response = self.client.get(
            reverse("projects:project_detail", args=[self.project_b.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_non_member_cannot_list_projects_from_other_team(self):
        self.client.login(email="outsider@e.com", password="Outsider123")
        response = self.client.get(
            reverse("projects:project_list_by_team", args=[self.team_b.pk])
        )
        self.assertEqual(response.status_code, 403)


class ProjectArchiveTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(
            email="admin@e.com", password="Admin123", role=User.ROLE_ADMIN
        )
        self.team = Team.objects.create(name="Backend")
        self.client.login(email="admin@e.com", password="Admin123")

    def test_archive_project(self):
        project = Project.objects.create(name="P1", team=self.team)
        self.client.post(reverse("projects:project_archive", args=[project.pk]))
        project.refresh_from_db()
        self.assertEqual(project.status, Project.STATUS_ARCHIVED)

    def test_reactivate_project(self):
        project = Project.objects.create(
            name="P1", team=self.team, status=Project.STATUS_ARCHIVED
        )
        self.client.post(reverse("projects:project_archive", args=[project.pk]))
        project.refresh_from_db()
        self.assertEqual(project.status, Project.STATUS_ACTIVE)

    def test_archived_projects_hidden_by_default(self):
        Project.objects.create(
            name="Active", team=self.team, status=Project.STATUS_ACTIVE
        )
        Project.objects.create(
            name="Archived", team=self.team, status=Project.STATUS_ARCHIVED
        )
        response = self.client.get(
            reverse("projects:project_list_by_team", args=[self.team.pk])
        )
        self.assertContains(response, "Active")
        self.assertNotContains(response, "Archived")

    def test_archived_projects_visible_with_filter(self):
        Project.objects.create(
            name="Archived", team=self.team, status=Project.STATUS_ARCHIVED
        )
        response = self.client.get(
            reverse("projects:project_list_by_team", args=[self.team.pk])
            + "?archived=1"
        )
        self.assertContains(response, "Archived")
