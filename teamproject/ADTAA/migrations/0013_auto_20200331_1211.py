# Generated by Django 3.0.3 on 2020-03-31 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ADTAA', '0012_delete_solution'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='class',
            name='start_time',
            field=models.TimeField(null=True),
        ),
    ]
