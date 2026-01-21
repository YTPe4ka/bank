from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('accounts/', views.accounts_list, name='accounts_list'),
    path('accounts/add/', views.add_account, name='add_account'),
    path('account/<int:pk>/', views.account_detail, name='account_detail'),
    path('account/<int:account_id>/add-transaction/', views.add_transaction, name='add_transaction'),
    path('recurring-payments/', views.recurring_payments, name='recurring_payments'),
    path('recurring-payments/add/', views.add_recurring_payment, name='add_recurring_payment'),
    path('recurring-payments/<int:pk>/edit/', views.edit_recurring_payment, name='edit_recurring_payment'),
    path('recurring-payments/<int:pk>/delete/', views.delete_recurring_payment, name='delete_recurring_payment'),
    path('statistics/', views.statistics, name='statistics'),
]
