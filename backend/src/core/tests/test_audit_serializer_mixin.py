import pytest
from django.db import connection, models
from rest_framework.test import APIRequestFactory

from core.serializers.audit_serializer_mixin import AuditSerializerMixin
from core.models.mixins import BaseModel


class DummyAuditModel(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "core"
        db_table = "test_dummy_audit_model"


class DummyAuditSerializer(AuditSerializerMixin):
    class Meta:
        model = DummyAuditModel
        fields = ["id", "name", "created_by", "updated_by"]
        read_only_fields = ["created_by", "updated_by"]


@pytest.fixture(scope="module", autouse=True)
def dummy_audit_model_table(django_db_setup, django_db_blocker):
    table_name = DummyAuditModel._meta.db_table

    with django_db_blocker.unblock():
        existing_tables = connection.introspection.table_names()
        with connection.schema_editor() as schema_editor:
            if table_name not in existing_tables:
                schema_editor.create_model(DummyAuditModel)

    yield

    with django_db_blocker.unblock():
        existing_tables = connection.introspection.table_names()
        with connection.schema_editor() as schema_editor:
            if table_name in existing_tables:
                schema_editor.delete_model(DummyAuditModel)


def make_request(user):
    factory = APIRequestFactory()
    req = factory.post('/')
    req.user = user
    return req


@pytest.mark.django_db
class TestAuditSerializerMixin:

    def test_created_by_and_updated_by_are_set_on_create(self, admin_user):
        serializer = DummyAuditSerializer(
            data={'name': 'Audit Test'},
            context={'request': make_request(admin_user)},
        )
        assert serializer.is_valid(), serializer.errors
        obj = serializer.save()
        assert obj.created_by == admin_user
        assert obj.updated_by == admin_user

    def test_updated_by_is_set_on_update(self, admin_user, financeiro_user):
        obj = DummyAuditModel.objects.create(name='Original')
        assert obj.created_by is None
        serializer = DummyAuditSerializer(
            obj,
            data={'name': 'Updated'},
            partial=True,
            context={'request': make_request(financeiro_user)},
        )
        assert serializer.is_valid(), serializer.errors
        serializer.save()
        obj.refresh_from_db()
        assert obj.updated_by == financeiro_user
