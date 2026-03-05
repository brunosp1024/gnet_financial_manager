def pytest_configure(config):
    """Use a fast password hasher for users tests only."""
    from django.conf import settings
    settings.PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
