# Generated by Django 5.1.6 on 2025-03-14 12:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Album",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("artist", models.CharField(max_length=255)),
                ("release_date", models.DateField(blank=True, null=True)),
                ("cover_url", models.URLField(blank=True, null=True)),
                ("added_on", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="WeeklyPick",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("week_start_date", models.DateField()),
                ("week_end_date", models.DateField()),
                ("selected_on", models.DateTimeField(auto_now_add=True)),
                (
                    "album",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="weekly_picks",
                        to="albums.album",
                    ),
                ),
            ],
        ),
    ]
