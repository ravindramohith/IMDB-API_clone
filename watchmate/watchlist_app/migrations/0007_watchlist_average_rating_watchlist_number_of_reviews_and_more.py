# Generated by Django 4.1.3 on 2022-12-03 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("watchlist_app", "0006_review_reviewed_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="watchlist",
            name="average_rating",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="watchlist",
            name="number_of_reviews",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="watchlist",
            name="type",
            field=models.CharField(
                choices=[("1", "Movie"), ("2", "Series")], default=None, max_length=1
            ),
            preserve_default=False,
        ),
    ]
