import pytest
from django.contrib.auth.models import AnonymousUser, Group
from rest_framework.test import APIRequestFactory

from core.permissions import GROUPS_PERMISSIONS, GroupPermission
from users.models import User
from users.tests.factories import UserFactory


'''
Sobre o parâmetro "request":

request é uma fixture interna que o próprio pytest injeta em cada teste,
e request.getfixturevalue() é a forma de acessar outras fixtures dinamicamente pelo nome.
Isso é útil para evitar a necessidade de declarar explicitamente cada fixture como parâmetro
do teste, especialmente quando queremos testar múltiplas combinações de usuários e permissões
sem precisar criar um teste separado para cada uma.
'''


class DummyView:
    permission_resource = None
    queryset = None
    action = None


class BrokenQuerysetView:
    action = "list"

    def get_queryset(self):
        raise RuntimeError("boom")


class GetQuerysetView:
    action = "list"

    def get_queryset(self):
        return User.objects.all()


@pytest.fixture
def rf():
    return APIRequestFactory()


def _request_with_user(rf, user=None):
    request = rf.get("/")
    request.user = user if user is not None else AnonymousUser()
    return request


@pytest.mark.django_db
class TestGroupPermission:
    def test_denies_unauthenticated_user(self, rf):
        permission = GroupPermission()
        view = DummyView()
        view.permission_resource = "users"
        view.action = "list"

        request = _request_with_user(rf)

        assert permission.has_permission(request, view) is False


    def test_resolves_resource_from_queryset_model(self, admin_user, rf):
        permission = GroupPermission()
        view = DummyView()
        view.queryset = User.objects.all()
        view.action = "list"

        request = _request_with_user(rf, admin_user)
        
        assert permission.has_permission(request, view) is True


    def test_resolves_resource_from_get_queryset(self, admin_user, rf):
        permission = GroupPermission()
        view = GetQuerysetView()

        request = _request_with_user(rf, admin_user)

        assert permission.has_permission(request, view) is True


    def test_denies_when_user_has_no_group(self, no_group_user, rf):
        permission = GroupPermission()
        view = DummyView()
        view.permission_resource = "users"
        view.action = "list"

        request = _request_with_user(rf, no_group_user)

        assert permission.has_permission(request, view) is False


    def test_denies_when_resource_is_missing(self, admin_user, rf):
        permission = GroupPermission()
        view = DummyView()
        view.action = "list"

        request = _request_with_user(rf, admin_user)

        assert permission.has_permission(request, view) is False


    def test_denies_when_action_is_missing(self, admin_user, rf):
        permission = GroupPermission()
        view = DummyView()
        view.permission_resource = "users"

        request = _request_with_user(rf, admin_user)

        assert permission.has_permission(request, view) is False


    def test_get_resource_returns_none_when_get_queryset_fails(self):
        permission = GroupPermission()
        view = BrokenQuerysetView()

        assert permission._get_resource(view) is None
    

    def test_allows_when_any_group_has_permission(self, rf):
        permission = GroupPermission()
        view = DummyView()
        view.permission_resource = "users"
        view.action = "create"

        user = UserFactory(groups=["FINANCEIRO", "ADMIN"])
        request = _request_with_user(rf, user)

        assert permission.has_permission(request, view) is True


    def test_denies_when_user_group_is_not_mapped(self, rf):
        permission = GroupPermission()
        view = DummyView()
        view.permission_resource = "users"
        view.action = "list"

        group, _ = Group.objects.get_or_create(name="ESTAGIARIO")
        user = UserFactory(groups=[])
        user.groups.add(group)

        request = _request_with_user(rf, user)

        assert permission.has_permission(request, view) is False


    def test_denies_when_resource_is_not_mapped(self, admin_user, rf):
        permission = GroupPermission()
        view = DummyView()
        view.permission_resource = "reports"
        view.action = "list"

        request = _request_with_user(rf, admin_user)

        assert permission.has_permission(request, view) is False


    def test_denies_when_action_is_not_mapped(self, admin_user, rf):
        permission = GroupPermission()
        view = DummyView()
        view.permission_resource = "users"
        view.action = "approve"

        request = _request_with_user(rf, admin_user)

        assert permission.has_permission(request, view) is False


    def test_permission_resource_takes_precedence_over_queryset(self, financeiro_user, rf):
        permission = GroupPermission()
        view = DummyView()
        view.permission_resource = "customers"
        view.queryset = User.objects.all()
        view.action = "create"

        request = _request_with_user(rf, financeiro_user)

        assert permission.has_permission(request, view) is True


    def test_permissions_to_all_resources_and_actions(self, request, rf):
        permission = GroupPermission()
        view = DummyView()
        user_group_pairs = [
            ("admin_user", "ADMIN"),
            ("gerente_user", "GERENTE"),
            ("financeiro_user", "FINANCEIRO"),
        ]
        actions = ["list", "retrieve", "create", "update", "partial_update", "destroy", "me"]
        resources = ["users", "employees", "customers", "transactions", "notifications"]

        for user_fixture, group_name in user_group_pairs:
            user = request.getfixturevalue(user_fixture)
            http_request = _request_with_user(rf, user)
            for resource in resources:
                allowed_actions = set(GROUPS_PERMISSIONS[group_name].get(resource, []))
                for action in actions:
                    view.permission_resource = resource
                    view.action = action
                    is_allowed = permission.has_permission(http_request, view)
                    expected = action in allowed_actions
                    assert is_allowed is expected, (
                        f"group={group_name}, resource={resource}, action={action}, "
                        f"expected={expected}, got={is_allowed}"
                    )


    @pytest.mark.parametrize("group", ["ADMIN", "GERENTE", "FINANCEIRO"])
    def test_all_declared_permissions_are_allowed(self, request, rf, group):
        permission = GroupPermission()
        user = request.getfixturevalue(f"{group.lower()}_user")
        http_request = _request_with_user(rf, user)

        for resource, actions in GROUPS_PERMISSIONS[group].items():
            for action in actions:
                view = DummyView()
                view.permission_resource = resource
                view.action = action
                assert permission.has_permission(http_request, view) is True
