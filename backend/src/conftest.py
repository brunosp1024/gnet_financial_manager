import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import Group


# ── Groups ────────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True, scope='session')
def create_groups(django_db_setup, django_db_blocker):
    """Creates the groups once for the entire test session."""
    with django_db_blocker.unblock():
        for name in ('ADMIN', 'GERENTE', 'FINANCEIRO'):
            Group.objects.get_or_create(name=name)


# ── Users by Group ────────────────────────────────────────────────────────

@pytest.fixture
def admin_user(db):
    from users.tests.factories import UserFactory
    return UserFactory(groups=['ADMIN'])

@pytest.fixture
def gerente_user(db):
    from users.tests.factories import UserFactory
    return UserFactory(groups=['GERENTE'])

@pytest.fixture
def financeiro_user(db):
    from users.tests.factories import UserFactory
    return UserFactory(groups=['FINANCEIRO'])

@pytest.fixture
def no_group_user(db):
    from users.tests.factories import UserFactory
    return UserFactory(groups=[])


# ── Authenticated Clients ──────────────────────────────────────────────────────

@pytest.fixture
def api_client():
    return APIClient()

def make_auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def admin_client(admin_user):
    return make_auth_client(admin_user)

@pytest.fixture
def gerente_client(gerente_user):
    return make_auth_client(gerente_user)

@pytest.fixture
def financeiro_client(financeiro_user):
    return make_auth_client(financeiro_user)

@pytest.fixture
def no_group_client(no_group_user):
    return make_auth_client(no_group_user)
