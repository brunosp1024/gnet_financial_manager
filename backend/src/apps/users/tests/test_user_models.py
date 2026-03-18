import pytest
from apps.users.models import User


@pytest.mark.django_db
def test_user_str():
    user = User.objects.create(first_name="Bruno", last_name="Silva", username="bruno.silva")
    assert str(user) == "Bruno Silva"
