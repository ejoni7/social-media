# Generated by Django 4.0.6 on 2022-09-18 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0010_alter_topic_total_responses'),
    ]

    operations = [
        migrations.CreateModel(
            name='MostReact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(auto_now_add=True)),
                ('topic_title', models.CharField(max_length=70)),
                ('topic_id', models.PositiveIntegerField()),
            ],
        ),
    ]