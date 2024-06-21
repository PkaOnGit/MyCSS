from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re

class MaximumLengthValidator:
    def __init__(self, max_length=12):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                _("This password is too long. It must contain no more than %(max_length)d characters."),
                code='password_too_long',
                params={'max_length': self.max_length},
            )

    def get_help_text(self):
        return _("Your password must contain no more than %(max_length)d characters.") % {'max_length': self.max_length}

class CustomAttributeSimilarityValidator:
    """
    Validate whether the password is sufficiently different from the user's attributes.
    """

    def __init__(self, user_attributes=None, max_similarity=0.7):
        if user_attributes is None:
            user_attributes = ['username', 'email']
        self.user_attributes = user_attributes
        self.max_similarity = max_similarity

    def validate(self, password, user=None):
        if not user:
            return

        for attribute in self.user_attributes:
            value = getattr(user, attribute, None)
            if value and self._is_too_similar(password, value):
                raise ValidationError(
                    _("The password is too similar to the %(attribute)s."),
                    code='password_too_similar',
                    params={'attribute': attribute},
                )

    def _is_too_similar(self, password, value):
        value = value.lower()
        password = password.lower()

        # Check for substring
        if value in password or password in value:
            return True

        # Check for common character proportion
        common_chars = set(value) & set(password)
        similarity_ratio = len(common_chars) / max(len(value), len(password))
        return similarity_ratio >= self.max_similarity

    def get_help_text(self):
        return _(
            "Your password can't be too similar to your username or email address."
        )