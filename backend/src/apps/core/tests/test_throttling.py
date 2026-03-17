import pytest
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.test import APIClient
from apps.core.throttling import LoginRateThrottle


def _create_user(username='throttle-user', password='Senha@123'):
    user_model = get_user_model()
    return user_model.dm_objects.create_user(
        username=username,
        email=f'{username}@example.com',
        password=password,
    )


@pytest.fixture(autouse=True)
def _isolate_throttle_cache():
    cache.clear()
    yield
    cache.clear()


@pytest.mark.django_db
def test_token_endpoint_blocks_with_429_after_login_rate_is_exceeded(monkeypatch):
    user = _create_user()
    payload = {'username': user.username, 'password': 'Senha@123'}
    client = APIClient()
    monkeypatch.setattr(LoginRateThrottle, 'THROTTLE_RATES', {'login': '2/min'})

    assert client.post('/api/token/', payload, format='json').status_code == 200
    assert client.post('/api/token/', payload, format='json').status_code == 200
    assert client.post('/api/token/', payload, format='json').status_code == 429


@pytest.mark.django_db
def test_refresh_endpoint_not_blocked_by_login_throttle(monkeypatch):
    user = _create_user(username='refresh-user')
    payload = {'username': user.username, 'password': 'Senha@123'}
    client = APIClient()
    monkeypatch.setattr(LoginRateThrottle, 'THROTTLE_RATES', {'login': '1/min'})

    first = client.post('/api/token/', payload, format='json')
    assert first.status_code == 200

    # Consume the login quota to ensure throttling happens only on /api/token/.
    assert client.post('/api/token/', payload, format='json').status_code == 429

    refresh_payload = {'refresh': first.data['refresh']}
    refresh_response = client.post('/api/token/refresh/', refresh_payload, format='json')
    assert refresh_response.status_code == 200


@pytest.mark.django_db
def test_login_throttle_allows_requests_again_after_window(monkeypatch):
    user = _create_user(username='window-user')
    payload = {'username': user.username, 'password': 'Senha@123'}
    client = APIClient()
    now = [0.0]

    monkeypatch.setattr(LoginRateThrottle, 'timer', lambda _self: now[0])
    monkeypatch.setattr(LoginRateThrottle, 'THROTTLE_RATES', {'login': '1/min'})

    assert client.post('/api/token/', payload, format='json').status_code == 200
    assert client.post('/api/token/', payload, format='json').status_code == 429

    now[0] = 61.0
    assert client.post('/api/token/', payload, format='json').status_code == 200