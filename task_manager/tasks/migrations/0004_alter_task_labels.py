# Generated by Django 5.2.4 on 2025-07-18 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('tasks', '0003_alter_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(blank=True, related_name='tasks', to='labels.label', verbose_name='Метки'),
        ),
    ]
