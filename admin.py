import imp
from django.contrib import admin
from .models import Account, ExpenseType, IncomeType, Transaction, Expense


admin.site.register(ExpenseType)
admin.site.register(IncomeType)
admin.site.register(Account)
admin.site.register(Expense)
admin.site.register(Transaction)
