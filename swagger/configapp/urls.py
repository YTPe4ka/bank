from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.landing_or_redirect, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('set-language/', views.set_language, name='set_language'),
    
    # Dashboard and main views
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accounts/', views.accounts_list, name='accounts_list'),
    path('accounts/add/', views.add_account, name='add_account'),
    path('account/<int:pk>/', views.account_detail, name='account_detail'),
    path('account/<int:account_id>/add-transaction/', views.add_transaction, name='add_transaction'),
    path('categories/', views.categories_list, name='categories_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('recurring-payments/', views.recurring_payments, name='recurring_payments'),
    path('recurring-payments/add/', views.add_recurring_payment, name='add_recurring_payment'),
    path('recurring-payments/<int:pk>/edit/', views.edit_recurring_payment, name='edit_recurring_payment'),
    path('recurring-payments/<int:pk>/delete/', views.delete_recurring_payment, name='delete_recurring_payment'),
    path('statistics/', views.statistics, name='statistics'),
]
