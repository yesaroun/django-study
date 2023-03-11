import datetime

from django.db import models
from common.models import CommonModel


class Experience(CommonModel):

    """Experience Model Definition"""

    country: str = models.CharField(
        max_length=50,
        default="한국",
    )
    city: str = models.CharField(
        max_length=80,
        default="서울",
    )
    name: str = models.CharField(
        max_length=250,
    )
    host = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    price: int = models.PositiveIntegerField()
    address: str = models.CharField(max_length=250)
    start: datetime = models.TimeField()
    end: datetime = models.TimeField()
    description: str = models.TextField()
    perks = models.ManyToManyField(
        "experiences.Perk",
    )

    def __str__(self) -> str:
        return self.name


class Perk(CommonModel):

    """What is included Experience"""

    name: str = models.CharField(
        max_length=100,
    )
    details: str = models.CharField(
        max_length=250,
        blank=True,
        default="",
    )
    explanation: str = models.TextField(
        blank=True,
        default="",
    )

    def __str__(self) -> str:
        return self.name
