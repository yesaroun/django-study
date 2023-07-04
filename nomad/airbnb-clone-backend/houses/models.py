from django.db import models


# Create your models here.
class House(models.Model):
    """House Model"""

    name = models.CharField(max_length=140)
    price_per_night = models.PositiveIntegerField(
        verbose_name="Prices", help_text="Positive Numbers Only"
    )
    description = models.TextField()
    address = models.CharField(max_length=140)
    pets_allowed = models.BooleanField(
        default=True,
        verbose_name="Pets Allowed?",
        help_text="Does this house allow pets?",
    )

    def __str__(self) -> str:
        return self.name + ""
