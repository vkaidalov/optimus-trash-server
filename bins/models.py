from functools import partial
from django.core import validators
from django.db import models
from django.utils import timezone
from optimus_trash_server.settings import AUTH_USER_MODEL
from .tokens import generate_token


class Bin(models.Model):
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name='bins',
        on_delete=models.CASCADE
    )
    token = models.CharField(
        max_length=64,
        default=partial(generate_token, 64)
    )
    date_created = models.DateTimeField(
        default=timezone.now
    )
    longitude = models.FloatField(
        validators=[
            validators.MinValueValidator(-180.0),
            validators.MaxValueValidator(180.0)
        ]
    )
    latitude = models.FloatField(
        validators=[
            validators.MinValueValidator(-90.0),
            validators.MaxValueValidator(90.0)
        ]
    )
    max_weight = models.FloatField(
        validators=[
            validators.MinValueValidator(1.0)
        ]
    )
    current_weight = models.FloatField(
        default=0.0
    )

    def __str__(self):
        return "id: {}; coords: {}:{}; fullness: {}/{}".format(
            str(self.id),
            str(self.longitude),
            str(self.latitude),
            str(self.current_weight),
            str(self.max_weight)
        )
