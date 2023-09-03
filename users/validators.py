import re
from django.core.exceptions import ValidationError

class SpaceValidator(object):
    def validate(self, password, user=None):
        if " " in password:
            raise ValidationError(
                "The password cannot contain spaces",
                code='password_no_space',
            )

    def get_help_text(self):
        return "The password cannot contain spaces"


class LengthValidator(object):
    def __init__(self, min_length=8, max_length=16):
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, password, user=None):
        if not self.max_length >= len(password) >= self.min_length:
            raise ValidationError(
                "The password must be 8-16 characters long",
                code='password_length',
                params={'min_length': self.min_length, 'max_length': self.max_length},
            )

    def get_help_text(self):
        return "The password must be 8-16 characters long"


class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall('\d', password):
            raise ValidationError(
                "The password must contain at least 1 digit, 0-9.",
                code='password_no_number',
            )

    def get_help_text(self):
        return "The password must contain at least 1 digit, 0-9."


class LetterValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Za-z]', password):
            raise ValidationError(
                "The password must contain at least 1 alphabet letter",
                code='password_no_letter',
            )

    def get_help_text(self):
        return "The password must contain at least 1 alphabet letter"


# class UppercaseValidator(object):
#     def validate(self, password, user=None):
#         if not re.findall('[A-Z]', password):
#             raise ValidationError(
#                 ("The password must contain at least 1 uppercase letter, A-Z."),
#                 code='password_no_upper',
#             )
#
#     def get_help_text(self):
#         return (
#             "Your password must contain at least 1 uppercase letter, A-Z."
#         )
#
#
# class LowercaseValidator(object):
#     def validate(self, password, user=None):
#         if not re.findall('[a-z]', password):
#             raise ValidationError(
#                 ("The password must contain at least 1 lowercase letter, a-z."),
#                 code='password_no_lower',
#             )
#
#     def get_help_text(self):
#         return (
#             "Your password must contain at least 1 lowercase letter, a-z."
#         )


class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall("[#$%&'()*+,-./:;<=>?@[\]^_`{|}~]", password):
            raise ValidationError(
                ("The password must contain at least 1 special character: " +
                  "#$%&'()*+,-./:;<=>?@[\]^_`{|}~"),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return (
            "Your password must contain at least 1 special character: " +
            "#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        )
