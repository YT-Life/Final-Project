# Generated by Django 4.1.2 on 2022-12-20 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lyt", "0003_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="images",
            name="pic",
            field=models.ImageField(upload_to="images/"),
        ),
    ]
