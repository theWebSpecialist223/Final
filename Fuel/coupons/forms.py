from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django import forms

from.models import Record, IssuedMonthly, ServiceIssue

# Register/ Create User
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

class AddCouponsForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['fuel_type', 'serial_number_group', 'quantity', 'supplier', 'purpose', 'amount_for_one']

class IssueMonthlyForm(forms.ModelForm):
    class Meta:
        model = IssuedMonthly
        fields = ['quantity', 'issued_to', 'coupon_group', 'amount_owing']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['coupon_group'].queryset = Record.objects.filter(purpose ='Monthly Allocation')

class ServiceIssueForm(forms.ModelForm):
    class Meta:
        model = ServiceIssue
        fields = ['issued_to', 'coupon_group', 'designation', 'department', 'reason', 'number_of_coupons', ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['coupon_group'].queryset = Record.objects.filter(purpose ='Condition Of Service')