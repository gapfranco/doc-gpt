# Generated by Django 4.2.11 on 2024-03-17 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0009_documentbody"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="document",
            name="file",
        ),
    ]
