# Generated by Django 3.2.6 on 2021-09-01 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]