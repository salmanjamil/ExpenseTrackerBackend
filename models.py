
from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from datetime import date

from django.utils import timezone


class ExpenseType(models.Model):
    title =  models.CharField(max_length=50)

    def __str__(self):
        return self.title

class IncomeType(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Account(models.Model):
    name = models.CharField(max_length= 20)
    balance = models.IntegerField(default= 0)
    daily_withdrawl_limit = models.IntegerField(default= None, blank= True, null= True)
    owner = models.ForeignKey(User, on_delete= models.DO_NOTHING)


class Transaction(models.Model):

    class TransactionType(models.TextChoices):
        INCOME = 'I'
        EXPENSE = 'E'

    transcation_date = models.DateField(auto_now_add = True)
    amount = models.IntegerField(default= 0)
    transaction_type = models.CharField(
        max_length= 1,
        choices= TransactionType.choices,
        default= TransactionType.EXPENSE
    )

    account = models.ForeignKey(Account, on_delete=  models.DO_NOTHING)

class Income(Transaction):
    income_type = models.ForeignKey(IncomeType, on_delete= models.DO_NOTHING)

class Expense(Transaction):
    expense_type = models.ForeignKey(ExpenseType, on_delete= models.DO_NOTHING)




