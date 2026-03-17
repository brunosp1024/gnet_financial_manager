import uuid

import pytest
from django.db import connection, models
from django.utils import timezone

from apps.core.models.mixins import BaseModel


class DummyModel(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default="dummy")

    class Meta:
        app_label = "core"
        db_table = "test_dummy_model_for_mixins"


@pytest.fixture(scope="session", autouse=True)
def dummy_model_table(django_db_setup, django_db_blocker):
    table_name = DummyModel._meta.db_table

    with django_db_blocker.unblock():
        existing_tables = connection.introspection.table_names()
        with connection.schema_editor() as schema_editor:
            if table_name not in existing_tables:
                schema_editor.create_model(DummyModel)

    yield

    with django_db_blocker.unblock():
        existing_tables = connection.introspection.table_names()
        with connection.schema_editor() as schema_editor:
            if table_name in existing_tables:
                schema_editor.delete_model(DummyModel)


@pytest.mark.django_db
class TestDeletedMixin:
    def test_soft_delete_marks_deleted_at(self):
        obj = DummyModel.dm_objects.create(name="A")
        assert obj.deleted_at is None

        before = timezone.now()
        obj.delete()
        obj.refresh_from_db()

        assert obj.deleted_at is not None
        assert obj.deleted_at >= before

    def test_default_manager_hides_soft_deleted(self):
        obj = DummyModel.dm_objects.create(name="B")
        pk = obj.pk
        obj.delete()

        assert not DummyModel.objects.filter(pk=pk).exists()
        assert DummyModel.dm_objects.filter(pk=pk).exists()

    def test_hard_delete_removes_row(self):
        obj = DummyModel.dm_objects.create(name="C")
        pk = obj.pk

        obj.hard_delete()

        assert not DummyModel.dm_objects.filter(pk=pk).exists()


@pytest.mark.django_db
class TestTimestampableMixin:
    def test_id_is_uuid(self):
        obj = DummyModel.dm_objects.create(name="UUID")
        assert isinstance(obj.pk, uuid.UUID)

    def test_created_at_is_filled(self):
        obj = DummyModel.dm_objects.create(name="D")
        assert obj.created_at is not None

    def test_updated_at_changes_on_save(self):
        obj = DummyModel.dm_objects.create(name="E")
        before = obj.updated_at

        obj.name = "E2"
        obj.save(update_fields=["name"])
        obj.refresh_from_db()

        assert obj.updated_at >= before
