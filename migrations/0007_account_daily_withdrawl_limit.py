# Generated by Django 3.2.12 on 2022-04-11 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenseTracker', '0006_account_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='daily_withdrawl_limit',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
