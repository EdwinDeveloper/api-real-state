# Generated by Django 4.0.10 on 2023-04-16 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_investment_ordinary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='ordinary',
            field=models.IntegerField(null=True),
        ),
    ]
