# Generated by Django 4.1.1 on 2022-12-13 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('intro', models.TextField()),
                ('regdate', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
