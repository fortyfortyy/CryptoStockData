from six import text_type
# generate token
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# ---
from users.models import UserProfile


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: UserProfile, timestamp) -> str:
        return (
                text_type(user.pk) + text_type(timestamp) +
                text_type(user.is_active)
        )


account_token = TokenGenerator()
