# Generated by Django 2.2 on 2020-01-30 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20200130_0624'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidatepics',
            name='user',
        ),
    ]
