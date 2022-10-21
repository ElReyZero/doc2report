# Generated by Django 3.2.16 on 2022-10-13 00:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('pet_filter', models.BooleanField()),
                ('rental_filter', models.BooleanField()),
                ('bbq_filter', models.BooleanField()),
                ('smoking_filter', models.BooleanField()),
                ('document', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='documents.document')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]