# Generated by Django 4.1.2 on 2022-12-16 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("lyt", "0002_delete_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="Images",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("pic", models.ImageField(upload_to="usr/%y")),
                ("comment", models.TextField()),
            ],
        ),
    ]
