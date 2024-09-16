# Generated by Django 5.0.6 on 2024-07-06 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0006_alter_user_middle_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invitecode",
            name="role",
            field=models.CharField(choices=[("admin", "admin"), ("user", "user")], max_length=5),
        ),
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[("admin", "admin"), ("user", "user")], default="user", max_length=5, verbose_name="role"
            ),
        ),
    ]
