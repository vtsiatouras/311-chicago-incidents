# Generated by Django 3.1.3 on 2020-11-25 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chicago_incidents', '0002_auto_20201125_1359'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='rodentbaitingpremises',
            index=models.Index(fields=['number_of_premises_baited'], name='rodent_bait_number__2d0558_idx'),
        ),
        migrations.AddIndex(
            model_name='rodentbaitingpremises',
            index=models.Index(fields=['number_of_premises_w_garbage'], name='rodent_bait_number__fc5a64_idx'),
        ),
        migrations.AddIndex(
            model_name='rodentbaitingpremises',
            index=models.Index(fields=['number_of_premises_w_rats'], name='rodent_bait_number__fe14b9_idx'),
        ),
    ]
