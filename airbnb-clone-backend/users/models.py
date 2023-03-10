from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE: tuple = ("male", "Male")  # (db값, admin패널에서 보이는 label)
        FEMALE: tuple = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        KR: tuple = ("kr", "Korean")
        EN: tuple = ("en", "English")

    class CurrencyChoices(models.TextChoices):
        WON: tuple = "won", "Korean Won"
        USD: tuple = "usd", "Dollar"

    first_name: str = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name: str = models.CharField(
        max_length=150,
        editable=False,
    )
    avatar = models.ImageField(
        blank=True,
    )
    name: str = models.CharField(
        max_length=150,
        default="",
    )
    is_host: bool = models.BooleanField(
        default=False,
    )
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
    )
    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
    )
    currency = models.CharField(
        max_length=5,
        choices=CurrencyChoices.choices,
    )
