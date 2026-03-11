import pytest
from notifications.models import Notification
from notifications.tests.factories import NotificationFactory

LIST_URL = '/api/notifications/'


def DETAIL_URL(pk):
    return f'/api/notifications/{pk}/'


# ── Authentication ─────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestNotificationViewsAuthentication:

    def test_unauthenticated_returns_401(self, api_client):
        assert api_client.get(LIST_URL).status_code == 401

    def test_no_group_returns_403(self, no_group_client):
        assert no_group_client.get(LIST_URL).status_code == 403


# ── Filters ────────────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestNotificationViewsFilters:

    def test_filter_by_is_read_false(self, admin_client):
        NotificationFactory(is_read=False)
        NotificationFactory(is_read=True)
        res = admin_client.get(LIST_URL, {'is_read': 'false'})
        assert res.status_code == 200
        assert all(not n['is_read'] for n in res.data['results'])

    def test_filter_by_is_read_true(self, admin_client):
        NotificationFactory(is_read=False)
        NotificationFactory(is_read=True)
        res = admin_client.get(LIST_URL, {'is_read': 'true'})
        assert res.status_code == 200
        assert all(n['is_read'] for n in res.data['results'])

    def test_filter_by_type(self, admin_client):
        NotificationFactory(type=Notification.Type.OVERDUE)
        NotificationFactory(type=Notification.Type.BIRTHDAY)
        res = admin_client.get(LIST_URL, {'type': 'OVERDUE'})
        assert res.status_code == 200
        assert all(n['type'] == 'OVERDUE' for n in res.data['results'])


# ── CRUD ───────────────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestNotificationViewsCRUD:

    def test_list_user(self, admin_client):
        NotificationFactory.create_batch(3)
        res = admin_client.get(LIST_URL)
        assert res.status_code == 200
        assert res.data['count'] >= 3

    def test_list_returns_expected_fields(self, admin_client):
        NotificationFactory()
        res = admin_client.get(LIST_URL)
        assert res.status_code == 200
        item = res.data['results'][0]
        assert set(item.keys()) == {'id', 'type', 'message', 'is_read', 'created_at'}

    def test_create_returns_201_with_correct_data(self, admin_client):
        data = {'type': 'NEW_CUSTOMER', 'message': 'Novo cliente cadastrado'}
        res = admin_client.post(LIST_URL, data)
        assert res.status_code == 201
        assert res.data['message'] == 'Novo cliente cadastrado'
        assert res.data['type'] == 'NEW_CUSTOMER'

    def test_retrieve_returns_notification(self, admin_client):
        n = NotificationFactory(message='Mensagem específica')
        res = admin_client.get(DETAIL_URL(n.pk))
        assert res.status_code == 200
        assert res.data['message'] == 'Mensagem específica'

    def test_partial_update_marks_as_read(self, admin_client):
        n = NotificationFactory(is_read=False)
        res = admin_client.patch(DETAIL_URL(n.pk), {'is_read': True})
        assert res.status_code == 200
        n.refresh_from_db()
        assert n.is_read is True

    def test_delete_removes_notification(self, admin_client):
        n = NotificationFactory()
        pk = n.pk
        res = admin_client.delete(DETAIL_URL(pk))
        assert res.status_code == 204
        assert not Notification.objects.filter(pk=pk).exists()
