# Generated by Django 4.0.6 on 2023-11-04 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0019_sametopics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sametopics',
            name='relateds',
            field=models.ManyToManyField(blank=True, to='topic.topic'),
        ),
    ]