# Generated by Django 4.0.6 on 2022-10-08 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0018_mostreact_topic_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='SameTopics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50)),
                ('relateds', models.ManyToManyField(blank=True, null=True, to='topic.topic')),
            ],
        ),
    ]
