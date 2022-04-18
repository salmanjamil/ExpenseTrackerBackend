from dataclasses import field, fields
from operator import mod
from pyexpat import model
from rest_framework import serializers
from expenseTracker import models
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ExpenseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExpenseType
        fields = ['id', 'title']

class IncomeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IncomeType
        fields = ['id', 'title']

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = ['id', 'name', 'balance', 'owner', 'daily_withdrawl_limit']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = ['id', 'transcation_date', 'amount', 'transaction_type', 'account']

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Income
        fields = ['id', 'transcation_date', 'amount', 'transaction_type', 'account', 'income_type']

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Expense
        fields = ['id', 'transcation_date', 'amount', 'transaction_type', 'account', 'expense_type']