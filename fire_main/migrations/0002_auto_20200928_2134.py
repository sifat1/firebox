# Generated by Django 2.2.7 on 2020-09-28 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fire_main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fire_info',
            name='brightness_temp',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='fire_info',
            name='date',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='fire_info',
            name='frp',
            field=models.TextField(),
        ),
    ]