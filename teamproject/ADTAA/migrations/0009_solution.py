# Generated by Django 3.0.3 on 2020-03-28 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ADTAA', '0008_auto_20200321_1508'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solution_id', models.CharField(blank=True, max_length=128, null=True)),
                ('course_title', models.ManyToManyField(to='ADTAA.Class')),
                ('last_name', models.ManyToManyField(to='ADTAA.Instructor')),
            ],
        ),
    ]