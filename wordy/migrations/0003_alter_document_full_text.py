# Generated by Django 4.0.1 on 2022-01-25 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wordy", "0002_alter_document_full_text_alter_document_name_and_more")
    ]

    operations = [
        migrations.AlterField(
            model_name="document",
            name="full_text",
            field=models.TextField(blank=True, default=""),
            preserve_default=False,
        )
    ]
