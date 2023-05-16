import string
from django.core.exceptions import ValidationError


def contains_special_character(value: str) -> bool:
    """value에 특수문자가 있는지 확인

    Args:
        value (str): 입력 문자열

    Returns:
        bool: 특수문자가 있는 경우 True
    """
    for char in value:
        if char in string.punctuation:
            return True
    return False


def contains_uppercase_letter(value: str) -> bool:
    """value에 영문 대문자가 있는지 확인

    Args:
        value (str): 입력 문자열

    Returns:
        bool: 대문자가 있는 경우 True
    """
    for char in value:
        if char.isupper():
            return True
    return False


def contains_lowercase_letter(value: str) -> bool:
    """value에 영문 소문자가 있는지 확인

    Args:
        value (str): 입력 문자열

    Returns:
        bool: 소문자가 있는 경우 True
    """
    for char in value:
        if char.islower():
            return True
    return False


def contains_number(value: str) -> bool:
    """value에 숫자가 있는지 확인

    Args:
        value (str): 입력 문자열

    Returns:
        bool: 숫자가 있는 경우 True
    """
    for char in value:
        if char.isdigit():
            return True
    return False


def validate_no_special_characters(value: str) -> ValidationError:
    """특수문자를 포함할 수 없음

    Args:
        value (str): 입력 문자열

    Raises:
        ValidationError
    """
    if contains_special_character(value):
        raise ValidationError("특수 문자를 포함할 수 없습니다.")


class CustomPasswordValidator:
    """8자 이상, 영문 대/소문자, 숫자 포함"""

    def validate(self, password: str, user=None):
        if (
            len(password) < 8
            or not contains_uppercase_letter(password)
            or not contains_lowercase_letter(password)
            or not contains_number(password)
        ):
            raise ValidationError("8자 이상이며 영문 대/소문자, 숫자를 포함해야 합니다.")

    def get_help_text(self):
        return "8자 이상이며 영문 대/소문자, 숫자를 포함해야 합니다."
