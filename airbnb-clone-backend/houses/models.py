from django.db import models


class House(models.Model):

    """Model Definition for Houses"""

    name: str = models.CharField(max_length=140)
    price_per_night: int = models.PositiveIntegerField(
        verbose_name="Price", help_text="Positive Numbers Only"
    )
    description: str = models.TextField()
    address: str = models.CharField(max_length=140)
    pets_allowed: bool = models.BooleanField(
        verbose_name="Pets Allowed?",
        default=True,
        help_text="Does this house allow pets?",
    )
    owner: int = models.ForeignKey("users.User", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
