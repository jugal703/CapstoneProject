from django.contrib.auth.password_validation import CommonPasswordValidator, \
    MinimumLengthValidator, \
    NumericPasswordValidator, \
    UserAttributeSimilarityValidator
from django.core.validators import validate_email
from django.forms import ValidationError
from django.utils.translation import ugettext as _

from ADTAA.globals import raise_unexpected_error

import ADTAA.models as base_models


class CustomPasswordValidator:

    def __init__(self, min_length=1):
        self.min_length = min_length

    def validate(self, password, user=None):
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if not any(char.isdigit() for char in password):
            raise ValidationError(_('Password must contain at least %(min_length)d digit.') % {'min_length': self.min_length})
        if not any(char.isalpha() for char in password):
            raise ValidationError(_('Password must contain at least %(min_length)d letter.') % {'min_length': self.min_length})
        if not any(char in special_characters for char in password):
            raise ValidationError(_('Password must contain at least %(min_length)d special character.') % {'min_length': self.min_length})

    def get_help_text(self):
        return ""


class NewUsernameValidator(object):

    def __call__(self, *args, **kwargs):
        self.validate(args[0])

    def validate(self, username):
        try:
            validate_email(username)
        except ValidationError:
            raise ValidationError(
                'Username %(username)s is invalid.',
                code='invalid',
                params={'username': username},
            )
        except Exception as e:
            raise_unexpected_error(e)

        # At this point, the username *might* be valid. The check above doesn't ensure that the name is available-
        # it only ensures that the name has the correct form (it doesn't have whitespace and only uses allowed
        # characters).

        # Let's count the number of WordyUser objects that have this username. Since usernames must be unique,
        # this value will either be 0 or 1. That's super nice because we can just return the result of our
        # WordyUser count and Django will treat a 0 as "falsy" and any other number as "truthy."
        username_in_use = base_models.BaseUser.objects.all().filter(username=username).count()
        if username_in_use:
            raise ValidationError(
                'Username %(username)s is already in use. Please choose another.',
                params={'username': username},
                code='invalid',
            )

        # If we get to this point, we know the username is valid and available. Validate functions need to return
        # the validated value on success
        return username


class PassWordUsernameValidator(object):

    def __call__(self, *args, **kwargs):
        self.validate(args[0])

    def validate(self, username):
        try:
            validate_email(username)
        except ValidationError:
            raise ValidationError(
                'Username %(username)s is invalid.',
                code='invalid',
                params={'username': username},
            )
        except Exception as e:
            raise_unexpected_error(e)

        # At this point, the username *might* be valid. The check above doesn't ensure that the name is available-
        # it only ensures that the name has the correct form (it doesn't have whitespace and only uses allowed
        # characters).

        # Let's count the number of WordyUser objects that have this username. Since usernames must be unique,
        # this value will either be 0 or 1. That's super nice because we can just return the result of our
        # WordyUser count and Django will treat a 0 as "falsy" and any other number as "truthy."
        username_in_use = base_models.BaseUser.objects.all().filter(username=username).count()
        if not username_in_use:
            raise ValidationError(
                'Username %(username)s do not exist. Please choose another.',
                params={'username': username},
                code='invalid',
            )

        # If we get to this point, we know the username is valid and available. Validate functions need to return
        # the validated value on success
        return username


class PasswordValidator(object):
    default_validators = [
        CustomPasswordValidator,
        CommonPasswordValidator,
        MinimumLengthValidator,
        NumericPasswordValidator,
        UserAttributeSimilarityValidator,
    ]

    def __call__(self, *args, **kwargs):
        self.validate(args[0])

    def validate(self, password):
        try:
            for validator in self.default_validators:
                validator().validate(password)
        except ValidationError as e:
            raise e
        except Exception as e:
            raise_unexpected_error(e)
