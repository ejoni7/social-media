# Generated by Django 4.0.6 on 2022-09-20 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0017_alter_rewarded_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='mostreact',
            name='topic_slug',
            field=models.SlugField(allow_unicode=True, blank=True, null=True),
        ),
    ]
