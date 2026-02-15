import random
import string

from django.db import IntegrityError

from short import models as short_models

ALPHABET: str = string.ascii_letters + string.digits


def _generate_code(length: int = 6) -> str:
    """
    Generate a random code
    Args:
        length: The length of the code
    Returns:
        code (str): The generated code
    """
    return "".join(random.choices(ALPHABET, k=length))


def create_short_url(original_url: str) -> tuple[short_models.ShortLink, bool]:
    """
    Create a short URL
    Args:
        original_url: The original URL to shorten
    Returns:
        short_link (short_models.ShortLink): The short link
        created (bool): True if the short link was created, False if it was retrieved
    """
    while True:
        try:
            code = _generate_code()
            return short_models.ShortLink.objects.get_or_create(
                original_url=original_url,
                defaults={"code": code}
            )
        except IntegrityError:
            continue