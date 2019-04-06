from django.db import models
from django.contrib.auth.models import User

from . import commons


class TargetUrl(models.Model):
    hash = models.CharField(max_length=24, null=False, unique=True)
    url = models.URLField(max_length=commons.TARGET_URL_MAX_LENGTH, null=False)

    def __repr__(self):
        return (
            f'<{self.__class__.__name__}: '
            f'hash={self.hash!r}, url={self.url!r}'
            f'>'
        )


class RedirectionKey(models.Model):
    key = models.CharField(max_length=commons.REDIRECTION_KEY_MAX_LENGTH, null=False, unique=True)
    target_url = models.ForeignKey(TargetUrl, on_delete=models.PROTECT)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return (
            f'<{self.__class__.__name__}: '
            f'key={self.key!r}, target_url={self.target_url!r}, user={self.owner!r}, is_active={self.is_active!r}'
            f'>'
        )
