# Generated by Django 4.0.10 on 2023-07-01 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_referral_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=True),
        ),
    ]
