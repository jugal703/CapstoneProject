# Generated by Django 3.0.3 on 2020-03-20 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ADTAA', '0004_auto_20200320_0023'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='instructor_id',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]