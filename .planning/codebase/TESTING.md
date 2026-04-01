# Testing Patterns

**Analysis Date:** 2026-04-01

## Test Framework

**Runner:**
- Django built-in test runner (via `python manage.py test`) in `projetinho/manage.py` and app-level `tests.py` files.
- Additional framework configs (`pytest`, `jest`, `vitest`): Not detected.

**Assertion Library:**
- `django.test.TestCase` assertions (`assertEqual`, `assertTrue`, `assertContains`, `assertRaises`) in `projetinho/accounts/tests.py`, `projetinho/projects/tests.py`, `projetinho/teams/tests.py`.

**Run Commands:**
```bash
python manage.py test              # Run all Django tests (projetinho)
python manage.py test accounts     # Run app-scoped tests (projetinho)
npm test                           # kube-news script currently fails intentionally
```

## Test File Organization

**Location:**
- Per-Django-app `tests.py` files under each app directory (examples: `projetinho/accounts/tests.py`, `projetinho/projects/tests.py`, `projetinho/teams/tests.py`, `projetinho/core/tests.py`).

**Naming:**
- File naming uses Django default single `tests.py` file per app.
- Test classes use `*Tests` suffix; test methods use `test_*` prefix.

**Structure:**
```
projetinho/
├── accounts/tests.py
├── teams/tests.py
├── projects/tests.py
└── core/tests.py
```

## Test Structure

**Suite Organization:**
```python
class ProjectPermissionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(...)

    def test_admin_can_create_project(self):
        self.client.login(email="admin@e.com", password="Admin123")
        response = self.client.post(reverse("projects:project_create", args=[self.team.pk]), {...})
        self.assertEqual(response.status_code, 302)
```
Source: `projetinho/projects/tests.py`

**Patterns:**
- Setup pattern: build fixtures in `setUp()` (users, teams, memberships, authenticated client).
- Teardown pattern: implicit DB rollback/cleanup from `TestCase`; no explicit `tearDown()` usage detected.
- Assertion pattern: combine HTTP status checks with DB-state checks (`refresh_from_db`, `exists`, queryset counts).

## Mocking

**Framework:**
- Not used in current repository tests (no `unittest.mock`, `pytest-mock`, or similar usage detected).

**Patterns:**
```python
with self.assertRaises(ValidationError):
    self.validator.validate('12345678')
```
Source: `projetinho/accounts/tests.py`

**What to Mock:**
- No established mock pattern yet; current tests prefer integration-style checks through ORM and request lifecycle.

**What NOT to Mock:**
- Do not mock Django ORM/auth for existing test style in `projetinho/*/tests.py`; tests validate real model constraints and permission flows.

## Fixtures and Factories

**Test Data:**
```python
self.team = Team.objects.create(name="Backend")
TeamMembership.objects.create(team=self.team, user=self.manager, is_manager=True)
```
Source: `projetinho/projects/tests.py`

**Location:**
- Inline object creation inside each test class `setUp()`; no dedicated fixture module or factory library detected.

## Coverage

**Requirements:**
- None enforced (no coverage config/tooling detected).

**View Coverage:**
```bash
Not configured in repository
```

## Test Types

**Unit Tests:**
- Model and validator behavior checks (`UserManager`, `LetterAndNumberValidator`, model `__str__`) in `projetinho/accounts/tests.py`, `projetinho/teams/tests.py`, `projetinho/projects/tests.py`.

**Integration Tests:**
- Request/response + auth/permission + DB mutation checks through Django `Client` in `projetinho/accounts/tests.py`, `projetinho/projects/tests.py`, `projetinho/teams/tests.py`.

**E2E Tests:**
- Not used.

## Common Patterns

**Async Testing:**
```python
Not used in current test suite (Django sync TestCase patterns only)
```

**Error Testing:**
```python
response = self.client.post(reverse('teams:team_create'), {'name': 'Backend'})
self.assertEqual(response.status_code, 200)  # form re-rendered with error
```
Source: `projetinho/teams/tests.py`

---

*Testing analysis: 2026-04-01*
