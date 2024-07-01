# Generated by Django 5.0.6 on 2024-07-01 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0003_alter_invitecode_created_by"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="invitecode",
            name="is_active",
        ),
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(max_length=30, verbose_name="first name"),
        ),
        migrations.AlterField(
            model_name="user",
            name="middle_name",
            field=models.CharField(max_length=30, verbose_name="middle name"),
        ),
    ]
