# shortener/utils.py
import string
from random import choices
from django.utils.crypto import get_random_string
from .models import ShortURL

ALPHABET = string.digits + string.ascii_letters  # 0-9a-zA-Z -> base62 charset

def base62_encode(num: int) -> str:
    if num == 0:
        return ALPHABET[0]
    arr = []
    base = len(ALPHABET)
    while num:
        num, rem = divmod(num, base)
        arr.append(ALPHABET[rem])
    arr.reverse()
    return ''.join(arr)

def generate_slug_for(instance=None, length=6):
    """
    Prefer using primary key + base62 for uniqueness if instance has id.
    For new objects without id, fallback to random string then ensure uniqueness.
    """
    # random fallback
    while True:
        slug = get_random_string(length=length, allowed_chars=ALPHABET)
        if not ShortURL.objects.filter(slug=slug).exists():
            return slug

def unique_slug_from_pk(pk: int):
    return base62_encode(pk)
