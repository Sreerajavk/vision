# Generated by Django 2.2 on 2020-01-30 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_candidatepics_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidatepics',
            name='user',
            field=models.IntegerField(),
        ),
    ]
