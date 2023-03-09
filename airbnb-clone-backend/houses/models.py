from django.db import models


class House(models.Model):

    """Model Definition for Houses"""

    name: str = models.CharField(max_length=140)
    price_per_night: int = models.PositiveIntegerField()
    description: str = models.TextField()
    address: str = models.CharField(max_length=140)
    pets_allowed: bool = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name
