from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone, translation
from django.db.models import Sum, Q
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from datetime import timedelta
from .models import Account, Transaction, Category, RecurringPayment
from .forms import TransactionForm, RecurringPaymentForm, AccountForm

def landing_or_redirect(request):
    """Главная страница - редирект на login если не авторизован"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

@require_http_methods(["GET", "POST"])
def login_view(request):
    """Страница входа"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Добро пожаловать!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    
    return render(request, 'configapp/login.html')

@require_http_methods(["GET", "POST"])
def register_view(request):
    """Страница регистрации"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if not all([username, email, password, password2]):
            messages.error(request, 'Пожалуйста, заполните все поля')
        elif password != password2:
            messages.error(request, 'Пароли не совпадают')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Это имя пользователя уже занято')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Этот email уже зарегистрирован')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, 'Аккаунт успешно создан!')
            return redirect('dashboard')
    
    return render(request, 'configapp/register.html')

@require_http_methods(["POST"])
def logout_view(request):
    """Выход из аккаунта"""
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта')
    return redirect('login')

def set_language(request):
    """Смена языка"""
    language = request.GET.get('language', 'en')
    if language in ['ru', 'uz', 'en']:
        translation.activate(language)
        request.session['django_language'] = language
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dashboard/'))

@login_required(login_url='login')
def dashboard(request):
    """Главная страница с обзором счетов"""

    accounts = Account.objects.filter(user=request.user)
    first_account = accounts.first()

    total_balance = accounts.aggregate(
        total=Sum('balance')
    )['total'] or 0

    # Последние 10 транзакций текущего пользователя
    recent_transactions = Transaction.objects.filter(
        account__user=request.user
    ).select_related('account', 'category').order_by('-date')[:10]

    # Сегодня
    today = timezone.now().date()

    today_expenses = Transaction.objects.filter(
        account__user=request.user,
        type='expense',
        date__date=today
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    today_income = Transaction.objects.filter(
        account__user=request.user,
        type='income',
        date__date=today
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    # Текущий месяц
    current_month_start = timezone.now().replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )

    month_expenses = Transaction.objects.filter(
        account__user=request.user,
        type='expense',
        date__gte=current_month_start
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    month_income = Transaction.objects.filter(
        account__user=request.user,
        type='income',
        date__gte=current_month_start
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'accounts': accounts,
        'first_account': first_account,
        'total_balance': total_balance,
        'recent_transactions': recent_transactions,
        'today_expenses': today_expenses,
        'today_income': today_income,
        'month_expenses': month_expenses,
        'month_income': month_income,
    }

    return render(request, 'configapp/dashboard.html', context)

def accounts_list(request):
    """Список всех счетов"""
    accounts = Account.objects.filter(user=request.user)
    total_balance = sum(acc.balance for acc in accounts)
    
    context = {
        'accounts': accounts,
        'total_balance': total_balance,
    }
    return render(request, 'configapp/accounts_list.html', context)


@login_required(login_url='login')
def add_account(request):
    """Добавление нового счета"""
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Счет успешно создан!')
            return redirect('accounts_list')
    else:
        form = AccountForm()
    
    context = {
        'form': form,
    }
    return render(request, 'configapp/add_account.html', context)


def account_detail(request, pk):
    """Детали счета с транзакциями"""
    account = get_object_or_404(Account, pk=pk, user=request.user)
    transactions = account.transactions.all()
    
    # Фильтрация по типу
    transaction_type = request.GET.get('type')
    if transaction_type:
        transactions = transactions.filter(type=transaction_type)
    
    # Фильтрация по категории
    category = request.GET.get('category')
    if category:
        transactions = transactions.filter(category_id=category)
    
    # Фильтрация по периоду
    period = request.GET.get('period', 'all')
    today = timezone.now().date()
    
    if period == 'today':
        transactions = transactions.filter(date__date=today)
    elif period == 'week':
        week_ago = today - timedelta(days=7)
        transactions = transactions.filter(date__date__gte=week_ago)
    elif period == 'month':
        month_start = today.replace(day=1)
        transactions = transactions.filter(date__date__gte=month_start)
    
    # Статистика
    expenses = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    
    categories = Category.objects.filter(transaction__account=account).distinct()
    
    context = {
        'account': account,
        'transactions': transactions,
        'categories': categories,
        'expenses': expenses,
        'income': income,
        'period': period,
    }
    return render(request, 'configapp/account_detail.html', context)


def add_transaction(request, account_id):
    """Добавление новой транзакции"""
    account = get_object_or_404(Account, pk=account_id, user=request.user)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            
            # Обновление баланса счета
            if transaction.type == 'income':
                account.balance += transaction.amount
            elif transaction.type == 'expense':
                account.balance -= transaction.amount
            account.save()
            
            messages.success(request, 'Транзакция успешно добавлена!')
            return redirect('account_detail', pk=account.id)
    else:
        form = TransactionForm()
    
    context = {
        'form': form,
        'account': account,
    }
    return render(request, 'configapp/add_transaction.html', context)


def recurring_payments(request):
    """Список регулярных платежей"""
    recurring = RecurringPayment.objects.filter(account__user=request.user)
    
    context = {
        'recurring_payments': recurring,
    }
    return render(request, 'configapp/recurring_payments.html', context)


def add_recurring_payment(request):
    """Добавление регулярного платежа"""
    if request.method == 'POST':
        form = RecurringPaymentForm(request.POST)
        if form.is_valid():
            recurring = form.save(commit=False)
            recurring.account.user = request.user
            recurring.save()
            messages.success(request, 'Регулярный платеж добавлен!')
            return redirect('recurring_payments')
    else:
        form = RecurringPaymentForm()
    
    context = {
        'form': form,
    }
    return render(request, 'configapp/add_recurring_payment.html', context)


def edit_recurring_payment(request, pk):
    """Редактирование регулярного платежа"""
    recurring = get_object_or_404(RecurringPayment, pk=pk, account__user=request.user)
    
    if request.method == 'POST':
        form = RecurringPaymentForm(request.POST, instance=recurring)
        if form.is_valid():
            form.save()
            messages.success(request, 'Платеж обновлен!')
            return redirect('recurring_payments')
    else:
        form = RecurringPaymentForm(instance=recurring)
    
    context = {
        'form': form,
        'recurring': recurring,
    }
    return render(request, 'configapp/add_recurring_payment.html', context)


@require_POST
def delete_recurring_payment(request, pk):
    """Удаление регулярного платежа"""
    recurring = get_object_or_404(RecurringPayment, pk=pk, account__user=request.user)
    recurring.delete()
    messages.success(request, 'Платеж удален!')
    return redirect('recurring_payments')


def statistics(request):
    """Статистика и графики"""
    today = timezone.now().date()
    month_start = today.replace(day=1)
    
    # Расходы по категориям за месяц для текущего пользователя
    expenses_by_category = Transaction.objects.filter(
        account__user=request.user,
        type='expense',
        date__date__gte=month_start
    ).values('category__name').annotate(sum=Sum('amount')).order_by('-sum')
    
    # Расходы по дням за месяц для текущего пользователя
    expenses_by_day = Transaction.objects.filter(
        account__user=request.user,
        type='expense',
        date__date__gte=month_start
    ).extra(select={'day': 'DATE(date)'}).values('day').annotate(sum=Sum('amount')).order_by('day')
    
    # Топ категорий за месяц для текущего пользователя
    top_categories = Transaction.objects.filter(
        account__user=request.user,
        type='expense',
        date__date__gte=month_start
    ).values('category__name', 'category__icon').annotate(
        sum=Sum('amount')
    ).order_by('-sum')[:5]
    
    total_expenses = Transaction.objects.filter(
        account__user=request.user,
        type='expense',
        date__date__gte=month_start
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    total_income = Transaction.objects.filter(
        account__user=request.user,
        type='income',
        date__date__gte=month_start
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'expenses_by_category': expenses_by_category,
        'expenses_by_day': expenses_by_day,
        'top_categories': top_categories,
        'total_expenses': total_expenses,
        'total_income': total_income,
    }
    return render(request, 'configapp/statistics.html', context)


def categories_list(request):
    """Список всех категорий"""
    categories = Category.objects.filter(user=request.user)
    expense_categories = categories.filter(type='expense')
    income_categories = categories.filter(type='income')
    
    context = {
        'categories': categories,
        'expense_categories': expense_categories,
        'income_categories': income_categories,
    }
    return render(request, 'configapp/categories_list.html', context)


def add_category(request):
    """Добавление новой категории"""
    if request.method == 'POST':
        name = request.POST.get('name')
        category_type = request.POST.get('type')
        icon = request.POST.get('icon', '📊')
        color = request.POST.get('color', '#FF6B6B')
        
        if name and category_type:
            category, created = Category.objects.get_or_create(
                user=request.user,
                name=name,
                type=category_type,
                defaults={'icon': icon, 'color': color}
            )
            if created:
                messages.success(request, f'Категория "{name}" успешно создана!')
            else:
                messages.info(request, f'Категория "{name}" уже существует!')
            return redirect('categories_list')
    
    context = {
        'types': Category.TYPE_CHOICES,
    }
    return render(request, 'configapp/add_category.html', context)
