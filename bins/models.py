from functools import partial
from django.core import validators
from django.db import models
from django.utils import timezone
from optimus_trash_server.settings import AUTH_USER_MODEL
from .tokens import generate_token

BIN_TOKEN_LENGTH = 64


class Bin(models.Model):
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name='bins',
        on_delete=models.CASCADE
    )
    token = models.CharField(
        max_length=BIN_TOKEN_LENGTH,
        default=partial(generate_token, BIN_TOKEN_LENGTH)
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
    fullness = models.FloatField(
        default=0.0
    )

    def refresh_token(self):
        self.token = generate_token(BIN_TOKEN_LENGTH)
        self.save()

    def save(self, *args, **kwargs):
        self.fullness = self.current_weight / self.max_weight
        super().save(*args, **kwargs)

    def __str__(self):
        return "id: {}; lat: {}; long: {}; fullness: {}/{}".format(
            str(self.id),
            str(self.latitude),
            str(self.longitude),
            str(self.current_weight),
            str(self.max_weight)
        )
