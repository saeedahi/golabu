import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class StrongPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                _("رمز عبور باید حداقل 8 کارکتر داشته باشد."),
                code='password_too_short'
            )
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("رمز عبور باید حداقل یک حروف بزرگ داشته باشد."),
                code='password_no_uppercase'
            )
        if not re.search(r'\d', password):
            raise ValidationError(
                _("رمز عبور باید حداقل یک عدد داشته باشد."),
                code='password_no_number'
            )
        if not re.search(r'[!@#$%^&*]', password):
            raise ValidationError(
                _("رمز عبور باید حداقل یک کاراکتر خاص (!@#$%^&*) داشته باشد."),
                code='password_no_special'
            )

    def get_help_text(self):
        return _(
            "رمز عبور باید حداقل ۸ کاراکتر، یک حرف بزرگ، یک عدد و یک کاراکتر خاص داشته باشد."
        )