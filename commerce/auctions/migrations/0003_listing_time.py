# Generated by Django 4.1.7 on 2023-03-21 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='time',
            field=models.TimeField(auto_now=True),
        ),
    ]
