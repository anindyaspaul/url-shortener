import hashlib
import base64
from typing import List

from django.contrib.auth.models import User

from .models import RedirectionKey, TargetUrl
from .commons import MAX_ACTIVE_REDIRECTION


def generate_url_hash(url: str) -> str:
    md5 = hashlib.md5(url.encode())
    md5_hash = md5.digest()
    b64_hash = base64.b64encode(md5_hash)
    return b64_hash.decode()


def add_url_redirection(owner: User, key: str, url: str):
    active_redirection_count = RedirectionKey.objects.filter(owner=owner, is_active=True).count()
    if active_redirection_count >= MAX_ACTIVE_REDIRECTION:
        print('Maximum number of urls reached.')
        return

    redirection_exists = RedirectionKey.objects.filter(key=key).exists()
    if redirection_exists:
        print('Redirection path unavailable.')
        return

    url_hash = generate_url_hash(url)
    target_url, _ = TargetUrl.objects.get_or_create(hash=url_hash, defaults={'url': url})
    redirection_key = RedirectionKey.objects.create(key=key, target_url=target_url, owner=owner)
    return redirection_key


def get_redirection_keys(owner: User, is_active=True) -> List[RedirectionKey]:
    return RedirectionKey.objects.filter(owner=owner, is_active=is_active).all()


def get_target_url(key: str) -> str:
    redirection_key = None
    try:
        redirection_key = RedirectionKey.objects.get(key=key)
    except RedirectionKey.DoesNotExist:
        pass
    if redirection_key is None:
        print(f'Redirection key {key} does not exist.')
        return None
    return redirection_key.target_url.url
