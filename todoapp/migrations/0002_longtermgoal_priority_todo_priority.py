# Generated by Django 5.1.4 on 2025-01-18 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='longtermgoal',
            name='priority',
            field=models.CharField(choices=[('high', 'Urgent and Important'), ('medium', 'Not Urgent but Important'), ('low', 'Urgent but Not Important'), ('lowest', 'Not Urgent and Not Important')], default='low', max_length=10),
        ),
        migrations.AddField(
            model_name='todo',
            name='priority',
            field=models.CharField(choices=[('high', 'Urgent and Important'), ('medium', 'Not Urgent but Important'), ('low', 'Urgent but Not Important'), ('lowest', 'Not Urgent and Not Important')], default='low', max_length=10),
        ),
    ]
