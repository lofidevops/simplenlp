# Generated by Django 4.0.1 on 2022-01-25 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("wordy", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="document", name="full_text", field=models.TextField(null=True)
        ),
        migrations.AlterField(
            model_name="document", name="name", field=models.SlugField(unique=True)
        ),
        migrations.AddConstraint(
            model_name="wordresult",
            constraint=models.UniqueConstraint(
                fields=("name", "document"), name="wordresult_name_document"
            ),
        ),
    ]
