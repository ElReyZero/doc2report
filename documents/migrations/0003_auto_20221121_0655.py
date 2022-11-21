# Generated by Django 3.2.16 on 2022-11-21 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_auto_20221121_0655'),
        ('documents', '0002_document_doc_page_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='doc_type',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='document',
            name='filters',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.report'),
            preserve_default=False,
        ),
    ]
