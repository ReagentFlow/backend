# Generated by Django 5.0.6 on 2024-10-03 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reagents", "0002_alter_container_container_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="container",
            name="cas",
        ),
        migrations.RemoveField(
            model_name="container",
            name="volume",
        ),
        migrations.AlterField(
            model_name="container",
            name="qualification",
            field=models.CharField(max_length=512),
        ),
    ]