# Generated by Django 4.0.4 on 2022-06-21 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0003_user_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
