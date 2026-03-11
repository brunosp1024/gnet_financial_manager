import pytest
from rest_framework.test import APIRequestFactory

from notifications.serializers import NotificationCreateSerializer, NotificationListSerializer
from notifications.models import Notification
from notifications.tests.factories import NotificationFactory


def make_request(user):
    factory = APIRequestFactory()
    req = factory.post('/')
    req.user = user
    return req


# ── NotificationCreateSerializer ──────────────────────────────────────────────

@pytest.mark.django_db
class TestNotificationCreateSerializer:

    def test_valid_data_creates_notification(self, admin_user):
        data = {'type': 'OVERDUE', 'message': 'Fatura em atraso', 'is_read': False}
        s = NotificationCreateSerializer(data=data, context={'request': make_request(admin_user)})
        assert s.is_valid(), s.errors
        n = s.save()
        assert n.pk is not None
        assert n.message == 'Fatura em atraso'
        assert n.type == Notification.Type.OVERDUE

    def test_missing_message_is_invalid(self, admin_user):
        data = {'type': 'ANOTHER'}
        s = NotificationCreateSerializer(data=data, context={'request': make_request(admin_user)})
        assert not s.is_valid()
        assert 'message' in s.errors

    def test_all_type_choices_are_valid(self, admin_user):
        for choice in Notification.Type.values:
            data = {'type': choice, 'message': f'Mensagem tipo {choice}'}
            s = NotificationCreateSerializer(data=data, context={'request': make_request(admin_user)})
            assert s.is_valid(), f"Tipo {choice} deveria ser válido: {s.errors}"


# ── NotificationListSerializer ─────────────────────────────────────────────────

@pytest.mark.django_db
class TestNotificationListSerializer:

    def test_returns_expected_fields(self):
        n = NotificationFactory()
        s = NotificationListSerializer(n)
        assert set(s.data.keys()) == {'id', 'type', 'message', 'is_read', 'created_at'}

    def test_is_read_defaults_to_false(self):
        n = NotificationFactory(is_read=False)
        s = NotificationListSerializer(n)
        assert s.data['is_read'] is False

    def test_many_serialization(self):
        NotificationFactory.create_batch(3)
        qs = Notification.objects.all()
        s = NotificationListSerializer(qs, many=True)
        assert len(s.data) == 3
