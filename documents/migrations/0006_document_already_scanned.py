# Generated by Django 3.2.16 on 2022-12-30 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0005_document_category_document_predictions'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='already_scanned',
            field=models.BooleanField(default=False),
        ),
    ]
