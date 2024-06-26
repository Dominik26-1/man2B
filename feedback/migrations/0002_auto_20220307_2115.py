# Generated by Django 3.2.7 on 2022-03-07 21:15

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='skill',
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rating', models.IntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)])),
                ('feedback', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='feedback.feedback')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='feedback.skill')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
