import re

from django.core.exceptions import ValidationError


class LetterAndNumberValidator:
    def validate(self, password, user=None):
        if not re.search(r'[a-zA-Z]', password):
            raise ValidationError('A senha deve conter pelo menos uma letra.')
        if not re.search(r'[0-9]', password):
            raise ValidationError('A senha deve conter pelo menos um número.')

    def get_help_text(self):
        return 'A senha deve conter pelo menos uma letra e um número.'
