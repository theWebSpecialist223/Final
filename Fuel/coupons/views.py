from django.shortcuts import render, redirect
from . forms import CreateUserForm, LoginForm, AddCouponsForm, IssueMonthlyForm, ServiceIssueForm
from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from . models import Record, IssuedMonthly, ServiceIssue

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Create your views here.
def home(request):
    return render(request, 'coupons/index.html')

# Register Users
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created Successfully")
            return redirect('my-login')

    context = {'form': form}
    return render(request, 'coupons/register.html', context=context)

def my_login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')

    context = {'form': form}
    return render(request, 'coupons/my_login.html', context=context)

# Dashboard
@login_required(login_url='my-login')
def dashboard(request):
    my_records = Record.objects.all()
    petrol_cos = Record.objects.filter(fuel_type='Petrol', purpose='Condition of Service')
    total_PE_cos = sum(Record.amount_in_litres for Record in petrol_cos)
    petrol_mo = Record.objects.filter(fuel_type='Petrol', purpose='Monthly Allocation')
    total_PE_mo = sum(Record.amount_in_litres for Record in petrol_mo)
    diesel_cos = Record.objects.filter(fuel_type='Diesel', purpose='Condition of Service')
    total_DI_cos = sum(Record.amount_in_litres for Record in diesel_cos)
    diesel_mo = Record.objects.filter(fuel_type='Diesel', purpose='Monthly Allocation')
    total_DI_mo = sum(Record.amount_in_litres for Record in diesel_mo)

    monthly_records = IssuedMonthly.objects.all()
 
    service_records = ServiceIssue.objects.all()

    
    context = {
        'records': my_records,
        'petrol_cos': petrol_cos,
        'total_PE_cos': total_PE_cos,
        'petrol_mo': petrol_mo,
        'total_PE_mo': total_PE_mo,
        'total_DI_cos': total_DI_cos,
        'total_DI_mo': total_DI_mo,
        'monthly_records': monthly_records,
        'service_records': service_records,
    }
    return render(request, 'coupons/dashboard.html', context=context)

# add Coupons
@login_required(login_url='my-login')
def add_coupons(request):
    form = AddCouponsForm()

    if request.method == 'POST':
        form = AddCouponsForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Coupons added")
            return redirect('dashboard')

    context = {'form': form}
    return render(request, 'coupons/addcoupons.html', context=context)

# - ISSUE COUPONS
@login_required(login_url='my-login')
def issue_coupons(request):
    form = IssueMonthlyForm()
    if request.method == 'POST':
        form = IssueMonthlyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Coupon Issued")
            return redirect('dashboard')
    
    context = {'form': form}
    return render(request, 'coupons/monthlyissue.html', context=context)

# Issue Coupon Condition of Service
@login_required(login_url='my-login')
def service_issue(request):
    form = ServiceIssueForm()
    if request.method == 'POST':
        form = ServiceIssueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Coupon Issued")
            return redirect('dashboard')

    context = {'form': form}
    return render(request, 'coupons/serviceIssue.html', context=context)



def user_logout(request):
    auth.logout(request)
    messages.success(request, "You have been logged out")
    return redirect("my-login")

# Generate Pdf file
def report_pdf(request):
    #Create Bytestream buffer
    buf = io.BytesIO()
    #create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    #create a text object
    textOb = c.beginText()
    textOb.setTextOrigin(inch, inch)
    textOb.setFont("Helvetica", 14)

    #add lines
    reports = Record.objects.all()

    lines = []

    for report in reports:
        lines.append(report.fuel_type)
        lines.append(report.serial_number_group)
        lines.append(report.purpose)
        lines.append('')



    for line in lines:
        textOb.textLine(line)
    
    #last part
    c.drawText(textOb)
    c.showPage()
    c.save()
    buf.seek(0)
    
    return FileResponse(buf, as_attachment=True, filename='repord.pdf')   