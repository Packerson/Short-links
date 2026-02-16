import random
import string

from django.db import IntegrityError

from short import models as short_models

ALPHABET: str = string.ascii_letters + string.digits


MAX_ATTEMPTS: int = 10
MIN_ATTEMPTS: int = 1
DEFAULT_ATTEMPTS: int = 3

DEFAULT_CODE_LENGTH: int = short_models.ShortLink.code.field.max_length


def _generate_code() -> str:
    """
    Generate a random code
    Code length is determined by the model field max_length
    Returns:
        code (str): The generated code
    """
    return "".join(random.choices(ALPHABET, k=DEFAULT_CODE_LENGTH))


def _validate_attempts(attempts: int | str | None) -> int:
    """
    Validate the number of attempts
    Args:
        attempts: The number of attempts to create a short link
    Returns:
        attempts: The validated number of attempts
    """
    if not isinstance(attempts, int):
        try:
            attempts = int(attempts)
        except (ValueError, TypeError):
            return DEFAULT_ATTEMPTS
    return min(max(attempts, MIN_ATTEMPTS), MAX_ATTEMPTS)


def create_short_url(
    original_url: str,
    attempts: int = DEFAULT_ATTEMPTS
) -> tuple[short_models.ShortLink | None, bool]:
    """
    Create a short URL
    Args:
        original_url: The original URL to shorten
        attempts: The number of attempts to create a short link
    Returns:
        short_link (short_models.ShortLink): The short link
        created (bool): True if the short link was created, False if it was retrieved
    """
    if not original_url or not isinstance(original_url, str):
        return None, False

    # validate attempts
    max_attempts = _validate_attempts(attempts)
    
    while max_attempts > 0:
        try:
            code = _generate_code()
            return short_models.ShortLink.objects.get_or_create(
                original_url=original_url,
                defaults={"code": code}
            )
        except IntegrityError:
            max_attempts -= 1
            continue
        except Exception as e:
            return None, False
    return None, False