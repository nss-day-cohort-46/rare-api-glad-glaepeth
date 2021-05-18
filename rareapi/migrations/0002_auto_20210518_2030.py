# Generated by Django 3.2.3 on 2021-05-18 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rareapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rareapi.rareuser'),
        ),
        migrations.AlterField(
            model_name='demotionqueue',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin', to='rareapi.rareuser'),
        ),
        migrations.AlterField(
            model_name='demotionqueue',
            name='approver_one',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approver', to='rareapi.rareuser'),
        ),
    ]
