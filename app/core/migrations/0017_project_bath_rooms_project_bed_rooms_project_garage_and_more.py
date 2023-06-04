# Generated by Django 4.0.10 on 2023-06-04 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_investment_ordinary'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='bath_rooms',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='bed_rooms',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='garage',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='gym',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='project',
            name='kitchen',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='pool',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='project',
            name='security',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='project',
            name='yoga',
            field=models.BooleanField(default=False),
        ),
    ]
