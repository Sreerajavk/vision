# Generated by Django 2.2 on 2020-02-06 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_auto_20200201_0536'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='api_key',
            field=models.CharField(default='sdkfjskfjsldkf', max_length=16),
            preserve_default=False,
        ),
    ]