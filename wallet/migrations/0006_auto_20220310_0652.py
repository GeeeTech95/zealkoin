# Generated by Django 3.0.5 on 2022-03-10 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0005_auto_20220310_0632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='plan_start',
            field=models.DateTimeField(),
        ),
    ]
