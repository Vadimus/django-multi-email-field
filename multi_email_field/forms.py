from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from multi_email_field.widgets import MultiEmailWidget


class MultiEmailField(forms.Field):
    message = _('Enter valid email addresses separated by commas.')
    code = 'invalid'
    widget = MultiEmailWidget

    def to_python(self, value):
        "Normalize data to a list of strings."
        # Return None if no input was given.
        if not value:
            return []
        # Deleting all CRs, spaces (repetitive too and commas)
        return [
            y.strip() for y in ",".join(
            [x for x in value.splitlines() if x != ""]).split(",") if y != ""]

    def validate(self, value):
        "Check if value consists only of valid emails."

        # Use the parent's handling of required fields, etc.
        super(MultiEmailField, self).validate(value)
        try:
            for email in value:
                validate_email(email)
        except ValidationError:
            raise ValidationError(self.message, code=self.code)
