# Generated by Django 5.0.4 on 2024-04-22 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admin_panel", "0009_remove_documentsigningrequest_document_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="documentsigningrequest",
            name="expires_at",
            field=models.DateTimeField(null=True),
        ),
    ]
