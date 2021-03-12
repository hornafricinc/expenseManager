from django.urls import path

from accounts import views
app_name='accounts'

urlpatterns=[
    path('',views.Index.as_view(),name='index'),
    path('signin/',views.log_user_in,name='signin'),
    path('registrations/new/',views.create_account,name='signup'),
    path('accounts/default/',views.user_dashboard,name='user_dashboard'),
    path('accounts/expenditure/', views.expenditure, name='expenditure'),
    path('accounts/expenditure/new_expenditure/', views.new_expenditure, name='new_expense'),

    path('accounts/revenue/', views.revenue_summary, name='revenue'),
    path('accounts/revenue/new_revenue/', views.new_revenue, name='new_revenue'),

]

