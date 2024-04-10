# Generated by Django 4.2.11 on 2024-04-09 15:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0013_alter_document_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="topic",
            name="publish",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user",
            name="query_credits",
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name="TopicInvite",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "topic",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.topic",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
