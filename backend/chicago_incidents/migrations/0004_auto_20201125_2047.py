# Generated by Django 3.1.3 on 2020-11-25 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chicago_incidents', '0003_auto_20201125_1649'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='incident',
            index=models.Index(fields=['completion_date'], name='incidents_complet_b8f19e_idx'),
        ),
    ]
