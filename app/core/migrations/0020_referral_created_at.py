# Generated by Django 4.0.10 on 2023-06-18 15:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_youtubeitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='referral',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
