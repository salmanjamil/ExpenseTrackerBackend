"""expenseTracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from expenseTracker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('expenseTypes/', views.expense_types),
    path('incomeTypes/', views.income_types),
    path('accounts/', views.accounts),
    path('income/', views.income),
    path('income/<int:account_id>', views.income_list),
    path('expense/<int:account_id>', views.expense_list),
    path('accountSummary/<int:accountID>', views.accountSummary),
    path('expense/', views.expense),
    path('users/', views.users),
    path('login/', views.login)
]
