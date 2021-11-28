# Generated by Django 3.2.9 on 2021-11-28 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('ISBN', models.CharField(max_length=13)),
                ('description', models.TextField()),
                ('published_date', models.DateTimeField()),
                ('num_pages', models.IntegerField()),
            ],
        ),
    ]