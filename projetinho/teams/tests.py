from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from teams.models import Team, TeamMembership

User = get_user_model()


class TeamModelTests(TestCase):
    def test_create_team(self):
        team = Team.objects.create(name='Backend', description='Time de backend')
        self.assertEqual(str(team), 'Backend')

    def test_team_name_unique(self):
        Team.objects.create(name='Backend')
        with self.assertRaises(Exception):
            Team.objects.create(name='Backend')

    def test_membership_str(self):
        team = Team.objects.create(name='Backend')
        user = User.objects.create_user(email='dev@e.com', password='Teste123')
        m = TeamMembership.objects.create(team=team, user=user, is_manager=False)
        self.assertIn('dev@e.com', str(m))
        self.assertIn('Membro', str(m))

    def test_membership_unique_together(self):
        team = Team.objects.create(name='Backend')
        user = User.objects.create_user(email='dev@e.com', password='Teste123')
        TeamMembership.objects.create(team=team, user=user)
        with self.assertRaises(Exception):
            TeamMembership.objects.create(team=team, user=user)


class TeamCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(
            email='admin@e.com', password='Admin123', role=User.ROLE_ADMIN
        )
        self.member = User.objects.create_user(
            email='membro@e.com', password='Membro123', role=User.ROLE_MEMBER
        )
        self.client.login(email='admin@e.com', password='Admin123')

    def test_admin_can_create_team(self):
        response = self.client.post(reverse('teams:team_create'), {
            'name': 'Frontend',
            'description': 'Time de front',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Team.objects.filter(name='Frontend').exists())

    def test_member_cannot_create_team(self):
        self.client.login(email='membro@e.com', password='Membro123')
        response = self.client.post(reverse('teams:team_create'), {
            'name': 'Hacked',
        })
        self.assertEqual(response.status_code, 403)

    def test_admin_can_edit_team(self):
        team = Team.objects.create(name='Old Name')
        response = self.client.post(reverse('teams:team_edit', args=[team.pk]), {
            'name': 'New Name',
            'description': '',
        })
        self.assertEqual(response.status_code, 302)
        team.refresh_from_db()
        self.assertEqual(team.name, 'New Name')

    def test_admin_can_delete_team(self):
        team = Team.objects.create(name='ToDelete')
        response = self.client.post(reverse('teams:team_delete', args=[team.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Team.objects.filter(name='ToDelete').exists())

    def test_duplicate_team_name_rejected(self):
        Team.objects.create(name='Backend')
        response = self.client.post(reverse('teams:team_create'), {
            'name': 'Backend',
        })
        self.assertEqual(response.status_code, 200)  # form re-rendered with error


class TeamVisibilityTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(
            email='admin@e.com', password='Admin123', role=User.ROLE_ADMIN
        )
        self.member = User.objects.create_user(
            email='membro@e.com', password='Membro123', role=User.ROLE_MEMBER
        )
        self.team_a = Team.objects.create(name='Team A')
        self.team_b = Team.objects.create(name='Team B')
        TeamMembership.objects.create(team=self.team_a, user=self.member, is_manager=False)

    def test_member_sees_only_their_teams(self):
        self.client.login(email='membro@e.com', password='Membro123')
        response = self.client.get(reverse('teams:team_list'))
        self.assertContains(response, 'Team A')
        self.assertNotContains(response, 'Team B')

    def test_admin_sees_all_teams(self):
        self.client.login(email='admin@e.com', password='Admin123')
        response = self.client.get(reverse('teams:team_list'))
        self.assertContains(response, 'Team A')
        self.assertContains(response, 'Team B')

    def test_member_cannot_access_other_team(self):
        self.client.login(email='membro@e.com', password='Membro123')
        response = self.client.get(reverse('teams:team_detail', args=[self.team_b.pk]))
        self.assertEqual(response.status_code, 404)

    def test_member_can_access_their_team(self):
        self.client.login(email='membro@e.com', password='Membro123')
        response = self.client.get(reverse('teams:team_detail', args=[self.team_a.pk]))
        self.assertEqual(response.status_code, 200)


class TeamMemberManagementTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(
            email='admin@e.com', password='Admin123', role=User.ROLE_ADMIN
        )
        self.user1 = User.objects.create_user(
            email='user1@e.com', password='User1234', role=User.ROLE_MEMBER
        )
        self.user2 = User.objects.create_user(
            email='user2@e.com', password='User2345', role=User.ROLE_MEMBER
        )
        self.team = Team.objects.create(name='Backend')
        self.membership = TeamMembership.objects.create(
            team=self.team, user=self.user1, is_manager=True
        )
        self.client.login(email='admin@e.com', password='Admin123')

    def test_add_member(self):
        response = self.client.post(
            reverse('teams:team_add_member', args=[self.team.pk]),
            {'user': self.user2.pk, 'is_manager': False},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TeamMembership.objects.filter(team=self.team, user=self.user2).exists())

    def test_add_duplicate_member(self):
        response = self.client.post(
            reverse('teams:team_add_member', args=[self.team.pk]),
            {'user': self.user1.pk},
        )
        self.assertEqual(response.status_code, 302)
        # Still only one membership
        self.assertEqual(TeamMembership.objects.filter(team=self.team, user=self.user1).count(), 1)

    def test_remove_member(self):
        m2 = TeamMembership.objects.create(team=self.team, user=self.user2, is_manager=False)
        response = self.client.post(
            reverse('teams:team_remove_member', args=[self.team.pk, m2.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TeamMembership.objects.filter(pk=m2.pk).exists())

    def test_cannot_remove_last_manager(self):
        response = self.client.post(
            reverse('teams:team_remove_member', args=[self.team.pk, self.membership.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TeamMembership.objects.filter(pk=self.membership.pk).exists())

    def test_cannot_demote_last_manager(self):
        response = self.client.post(
            reverse('teams:team_toggle_manager', args=[self.team.pk, self.membership.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.membership.refresh_from_db()
        self.assertTrue(self.membership.is_manager)

    def test_promote_member_to_manager(self):
        m2 = TeamMembership.objects.create(team=self.team, user=self.user2, is_manager=False)
        response = self.client.post(
            reverse('teams:team_toggle_manager', args=[self.team.pk, m2.pk])
        )
        m2.refresh_from_db()
        self.assertTrue(m2.is_manager)
