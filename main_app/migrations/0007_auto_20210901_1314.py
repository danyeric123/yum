# Generated by Django 3.2.6 on 2021-09-01 13:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main_app", "0006_auto_20210901_1307"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="name",
            field=models.TextField(default="recipe"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="recipe",
            name="owner",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name="Profile",
        ),
    ]
