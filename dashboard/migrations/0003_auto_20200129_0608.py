# Generated by Django 2.2 on 2020-01-29 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_staffverification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffverification',
            name='token',
            field=models.CharField(max_length=50),
        ),
    ]
