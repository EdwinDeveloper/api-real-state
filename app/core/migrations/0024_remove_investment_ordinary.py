# Generated by Django 4.0.10 on 2023-07-03 03:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_investment_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investment',
            name='ordinary',
        ),
    ]