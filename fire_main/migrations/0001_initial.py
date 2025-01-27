# Generated by Django 2.2.7 on 2020-09-28 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='fire_economic_data',
            fields=[
                ('city', models.TextField(primary_key=True, serialize=False)),
                ('country', models.TextField()),
                ('details', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='fire_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.TextField()),
                ('longitude', models.TextField()),
                ('city', models.TextField()),
                ('country', models.TextField()),
                ('brightness_temp', models.FloatField()),
                ('frp', models.FloatField()),
                ('date', models.DateField()),
            ],
        ),
    ]
