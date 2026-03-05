import pytest
from users.tests.factories import UserFactory


@pytest.mark.django_db
class TestUserModel:
    def test_create_user_with_correct_fields(self):
        user = UserFactory(first_name='João', last_name='Silva')
        assert user.pk is not None
        assert user.first_name == 'João'
        assert user.last_name == 'Silva'
        assert user.is_active is True
        assert user.created_at is not None
        assert user.updated_at is not None

    def test_str_returns_full_name(self):
        user = UserFactory(first_name='João', last_name='Silva')
        assert str(user) == 'João Silva'
