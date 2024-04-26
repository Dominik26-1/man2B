# Generated by Django 3.2.7 on 2022-04-12 20:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_alter_rating_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name_plural': 'Companies'},
        ),
        migrations.AlterModelOptions(
            name='employeemanagement',
            options={'verbose_name_plural': 'Employee Management'},
        ),
        migrations.RemoveField(
            model_name='company',
            name='avg_rating',
        ),
        migrations.RemoveField(
            model_name='department',
            name='avg_rating',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='avg_rating',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='avg_rating',
        ),
        migrations.RemoveField(
            model_name='position',
            name='avg_rating',
        ),
        migrations.RemoveField(
            model_name='project',
            name='avg_rating',
        ),
        migrations.RemoveField(
            model_name='skill',
            name='avg_rating',
        ),
        migrations.RemoveField(
            model_name='team',
            name='avg_rating',
        ),
    ]