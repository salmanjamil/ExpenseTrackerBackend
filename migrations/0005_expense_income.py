# Generated by Django 3.2.12 on 2022-04-10 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expenseTracker', '0004_auto_20220410_1109'),
    ]

    operations = [
        migrations.CreateModel(
            name='Income',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='expenseTracker.transaction')),
                ('income_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='expenseTracker.incometype')),
            ],
            bases=('expenseTracker.transaction',),
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='expenseTracker.transaction')),
                ('expense_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='expenseTracker.expensetype')),
            ],
            bases=('expenseTracker.transaction',),
        ),
    ]
