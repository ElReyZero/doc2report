# Generated by Django 3.2.16 on 2022-10-27 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_alter_report_predictions'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]