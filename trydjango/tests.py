from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.test import TestCase

class TryDjangoConfigTest(TestCase):
    def test_secret_key_strength(self):
        SECRET_KEY = settings.SECRET_KEY
        try:
            is_strong = validate_password(SECRET_KEY)
        except Exception as e:
            msg =  f'Weak secret key {e.messages}'
            self.fail(msg)