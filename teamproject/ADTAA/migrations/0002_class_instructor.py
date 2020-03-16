# Generated by Django 3.0.3 on 2020-03-15 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ADTAA', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_number', models.CharField(blank=True, max_length=128, null=True)),
                ('course_id', models.CharField(blank=True, max_length=128, null=True)),
                ('meeting_days', models.CharField(blank=True, choices=[('MW', 'Monday and Wednesday'), ('TR', 'Tuesday and Thursday')], max_length=128, null=True)),
                ('disciplines_areas', models.CharField(blank=True, choices=[('1', 'Programming - C++'), ('2', 'Programming - Python'), ('3', 'Game Development'), ('4', 'Data Structures and Algorithms'), ('5', 'Computer Organization'), ('6', 'Operating Systems'), ('7', 'Programming Languages'), ('8', 'Cybersecurity'), ('9', 'Mobile Applications'), ('10', 'Artificial Intelligence'), ('11', 'Networks'), ('12', 'Theory of Computation'), ('13', 'Parallel and Distributed Systems')], max_length=128, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(blank=True, max_length=128, null=True)),
                ('maximum_class_load', models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], max_length=128, null=True)),
                ('disciplines_areas', models.CharField(blank=True, choices=[('1', 'Programming - C++'), ('2', 'Programming - Python'), ('3', 'Game Development'), ('4', 'Data Structures and Algorithms'), ('5', 'Computer Organization'), ('6', 'Operating Systems'), ('7', 'Programming Languages'), ('8', 'Cybersecurity'), ('9', 'Mobile Applications'), ('10', 'Artificial Intelligence'), ('11', 'Networks'), ('12', 'Theory of Computation'), ('13', 'Parallel and Distributed Systems')], max_length=128, null=True)),
            ],
        ),
    ]