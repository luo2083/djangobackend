# Generated by Django 2.0 on 2020-10-31 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open_id', models.CharField(max_length=32, unique=True)),
                ('nickname', models.CharField(max_length=255)),
            ],
        ),
    ]
