# Generated by Django 3.2.12 on 2022-04-16 08:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenseTracker', '0007_account_daily_withdrawl_limit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='date',
        ),
        migrations.AddField(
            model_name='transaction',
            name='transcation_date',
            field=models.DateField(default=datetime.date(2022, 4, 16)),
        ),
    ]