from django import forms
from django.core import validators

from . import commons


class UrlSubmissionForm(forms.Form):
    url = forms.URLField(
        label='Target URL',
        max_length=commons.TARGET_URL_MAX_LENGTH,
        min_length=commons.TARGET_URL_MIN_LENGTH
    )
    key = forms.CharField(
        label='Shortened Path',
        max_length=commons.REDIRECTION_KEY_MAX_LENGTH,
        min_length=commons.REDIRECTION_KEY_MIN_LENGTH,
        validators=[validators.RegexValidator(
            regex='[A-Za-z0-9]+',
            message='Path can only contain alphabets and numbers.'
        )]
    )
