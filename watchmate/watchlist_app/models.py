from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class StreamPlatform(models.Model):
    name = models.CharField(max_length=20)
    about = models.CharField(max_length=50)
    web = models.URLField()

    def __str__(self):
        return self.name


class WatchList(models.Model):
    class Type(models.TextChoices):
        Movie = "1", "Movie"
        Series = "2", "Series"

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    platform = models.ForeignKey(
        StreamPlatform, on_delete=models.CASCADE, related_name="watchlist"
    )
    average_rating = models.FloatField(default=0)
    number_of_reviews = models.IntegerField(default=0)
    type = models.CharField(max_length=1, choices=Type.choices)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    reviewed_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    rating = models.PositiveBigIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    watchlist = models.ForeignKey(
        WatchList, on_delete=models.CASCADE, related_name="reviews"
    )
    description = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            "Review of " + str(self.reviewed_user) + " on " + str(self.watchlist.name)
        )
