# Generated by Django 3.2.3 on 2021-05-21 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rareapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(through='rareapi.PostTag', to='rareapi.Tag'),
        ),
    ]
