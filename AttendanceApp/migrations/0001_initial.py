# Generated by Django 4.0.5 on 2023-05-08 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PunchAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=50)),
                ('check_in', models.DateTimeField()),
                ('check_out', models.DateTimeField()),
            ],
        ),
    ]
