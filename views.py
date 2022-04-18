from cmath import exp
from datetime import date
from inspect import trace
from pickle import NONE
from django.http import JsonResponse
from .models import Account, Expense, ExpenseType, Income, IncomeType, Transaction
from .serializers import AccountSerializer, ExpenseSerializer, ExpenseTypeSerializer, IncomeSerializer, IncomeTypeSerializer, TransactionSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum

from expenseTracker import serializers

@api_view(['GET', 'POST'])
def expense_types(request):
    if request.method == 'GET':
        expenseTypes = ExpenseType.objects.all()
        serializer = ExpenseTypeSerializer(expenseTypes, many = True)
        return JsonResponse( serializer.data, safe = False)

    if request.method == 'POST':
        serializer = ExpenseTypeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status = status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def income_types(request):
    if request.method == 'GET':
        incomeTypes = IncomeType.objects.all()
        serializer = IncomeTypeSerializer(incomeTypes, many = True)
        return JsonResponse( {"income_types" : serializer.data}, safe = False)

    if request.method == 'POST':
        serializer = IncomeTypeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status = status.HTTP_201_CREATED)



@api_view(['GET', 'POST', 'PUT'])
@permission_classes([IsAuthenticated])
def accounts(request):
    if request.method == 'GET':
        print(request.user)
        accounts = Account.objects.filter(owner = request.user.id)
        serializer = AccountSerializer(accounts, many = True)
        return JsonResponse( serializer.data, safe = False)

    if request.method == 'POST':
        serializer = AccountSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status = status.HTTP_201_CREATED)

    if request.method == 'PUT':
        serializer = AccountSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def accountSummary(request, accountID):
    account = Account.objects.get(id = accountID)
    monthlyExpense = Expense.objects.filter(transcation_date__year = date.today().year, transcation_date__month = date.today().month, account = accountID)
    todaysExpenses = monthlyExpense.filter(transcation_date__day = date.today().day)
    monthlySum = monthlyExpense.aggregate(Sum('amount'))['amount__sum']
    todaySum = todaysExpenses.aggregate(Sum('amount'))['amount__sum']
    expenseByCategory = Expense.objects.filter(account = accountID).values('expense_type').annotate(dsum = Sum('amount')).order_by('-dsum')
    monthlyIncome = Income.objects.filter(transcation_date__year = date.today().year, transcation_date__month = date.today().month, account = accountID)
    todayIncome = monthlyIncome.filter(transcation_date__day = date.today().day)
    monthlyIncomeSum = monthlyIncome.aggregate(Sum('amount'))['amount__sum']
    todayIncomeSum = todayIncome.aggregate(Sum('amount'))['amount__sum']
    

    data = {
        "id": account.id,
        "title": account.name,
        "availableBalance": account.balance,
        "dailyWithdrawlLimit": account.daily_withdrawl_limit,
        "expensesToday": todaySum,
        "expensesThisMonth": monthlySum,
        "incomeToday": todayIncomeSum,
        "incomeThisMonth": monthlyIncomeSum 
    }

    expense_types = ExpenseType.objects.all()
    l = []
    for ele in expenseByCategory:
        exp = expense_types.get(id = ele['expense_type'])
        l.append(
            {
                'categoryTitle' : exp.title,
                'expense': ele['dsum']
            }
        )


    data['topSpendingCategories'] = l

    if data['expensesToday'] is None:
        data['expensesToday'] = 0
    if data['expensesThisMonth'] is None:
        data['expensesThisMonth'] = 0
    if data['incomeToday'] is None:
        data['incomeToday'] = 0
    if data['incomeThisMonth'] is None:
        data['incomeThisMonth'] = 0

    return JsonResponse(data)





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def income_list(request, account_id):
    incomes = Income.objects.filter(account = account_id)
    serializer = IncomeSerializer(incomes, many = True)
    return JsonResponse( serializer.data, safe = False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def expense_list(request, account_id):
    expenses = Expense.objects.filter(account = account_id)
    serializer = ExpenseSerializer(expenses, many = True)
    return JsonResponse( serializer.data, safe = False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def income(request):
    
    request.data['transaction_type'] = 'I'
    serializer = IncomeSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):

        account_id = request.data['account']
        amount = request.data['amount']
        account = Account.objects.filter(id = account_id).first()

        account.balance = account.balance + amount
        account.save()

        serializer.save()

        return Response(serializer.data, status = status.HTTP_201_CREATED)


@api_view(['GET'])
def users(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many = True)
        return JsonResponse( {"users" : serializer.data}, safe = False)


@api_view(['POST'])
def login(request):
    user = authenticate(username = request.data['username'], password = request.data['password'])
    if user is None:
        return Response(status= status.HTTP_401_UNAUTHORIZED)
    else:
        token = Token.objects.get(user= user)
        if token is None:
            token = Token.objects.create(user = user)
        return Response({'user_id' : user.id, 'token': token.key}, status = status.HTTP_200_OK)


@api_view(['POST'])
def expense(request):
    
    request.data['transaction_type'] = 'E'
    serializer = ExpenseSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):

        account_id = request.data['account']
        amount = request.data['amount']
        account = Account.objects.filter(id=account_id).first()

        if account.daily_withdrawl_limit is not None:
            expenses = Expense.objects.filter(transcation_date = date.today()).filter(account = account_id)
                 
            total_expense_today = 0
            for exp in expenses:
                total_expense_today += exp.amount
            
            if amount + total_expense_today > account.daily_withdrawl_limit:
                return Response('Transaction exceeds daily limit')

        if account.balance > amount:
            account.balance = account.balance - amount
            account.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
