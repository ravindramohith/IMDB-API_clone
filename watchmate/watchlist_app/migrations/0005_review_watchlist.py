# Generated by Django 4.1.3 on 2022-12-03 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("watchlist_app", "0004_review_watchlist_updatedat_alter_watchlist_created"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="watchlist",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews",
                to="watchlist_app.watchlist",
            ),
            preserve_default=False,
        ),
    ]