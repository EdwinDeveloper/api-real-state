# Generated by Django 4.0.10 on 2023-03-20 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_investment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='status',
            field=models.CharField(default='waiting', max_length=20),
        ),
    ]
