import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Sum
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView

from accounts.models import ExpenseManagerUser, Expenditure

class Index(TemplateView):
    template_name = 'index.html'
def log_user_in(request):
    if request.method == 'POST':
        email_address=request.POST['email']
        password=request.POST['password']
        user=authenticate(username=email_address,password=password)
        if user is not None:
            login(request,user)
            return redirect('accounts:user_dashboard')
        else:
            messages.error(request,"Wrong email/password combination.")
    return render(request,'login.html')


def create_account(request):
    if request.method == 'POST':
        email_address=request.POST['email']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        u_password=request.POST['password']
        real_password=make_password(u_password,salt=None)
        user=ExpenseManagerUser()
        user.email=email_address
        user.first_name=first_name
        user.last_name=last_name
        user.password=real_password
        user.is_active=True
        user.save()
        messages.success(request,"Your Account was successfully created. You can now Login")
    return render(request,'signup.html')
@login_required(login_url='accounts:index')
def user_dashboard(request):
    return render(request,'accounts/index.html')
@login_required(login_url='accounts:index')
def expenditure(request):
    all_expenses=Expenditure.objects.filter(donor=request.user).order_by('event_date')
    total_expenses=Expenditure.objects.filter(donor=request.user).aggregate(Sum('amount_spent'))
    total_events=Expenditure.objects.filter(donor=request.user).count()
    context={
        'expenditure':all_expenses,
        'total_expenditure':total_expenses,
        'total_events':total_events,
    }
    return render(request,'accounts/expenditure.html',context)
@login_required(login_url='accounts:index')
def new_expenditure(request):
    if request.method == 'POST':
        title=request.POST['e_title']
        e_category = request.POST['category']
        e_rname = request.POST['r_name']
        e_rphone = request.POST['r_phone']
        e_amount = request.POST['e_amount']
        payment_method = request.POST['payment_method']
        e_eventdatestr = request.POST['e_eventdate']
        datetimeobject=datetime.datetime.strptime(e_eventdatestr,'%b %d, %Y')
        e_eventdate=datetimeobject.date()

        expenditure=Expenditure()
        expenditure.title=title
        expenditure.category=e_category
        expenditure.recipient_name = e_rname
        expenditure.recipient_phone = e_rphone
        expenditure.amount_spent = e_amount
        expenditure.payement_method = payment_method
        expenditure.event_date = e_eventdate

        expenditure.donor = request.user
        expenditure.save()
        messages.success(request,"Expenditure Recorded Successfully")
    return render(request,'accounts/new_expense.html')