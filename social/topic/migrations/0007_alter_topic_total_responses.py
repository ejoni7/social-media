# Generated by Django 4.0.6 on 2022-09-15 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0006_alter_topic_total_responses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='total_responses',
            field=models.PositiveIntegerField(),
        ),
    ]
