# Generated by Django 4.0.10 on 2023-04-16 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_referral_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='ordinary',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
