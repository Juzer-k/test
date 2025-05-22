from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UsernameField,PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from burhanimart.models import ContactUs, CustomerAddress



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True,label='Email', widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {'username':forms.TextInput(attrs={'class':'form-control','autofocus': True})}



class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class':'form-control'}))
    password = forms.CharField(label='Password', strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class':'form-control'}))


class OldPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus':True,  'class':'form-control'}))
    new_password1 = forms.CharField(label='New Password', strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label='Confirm New Password', strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}))

class ForgotPasswordSendMail(PasswordResetForm):
    email = forms.EmailField(label='Email', max_length=150, widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class':'form-control'}))

class SetNewPassword(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label='Confirm New Password', strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}))

class Address(forms.ModelForm):
    # customer_name = forms.EmailField(label='Full Name', label_suffix = '-' , widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = CustomerAddress
        fields = ['customer_name', 'mobile_number', 'area_locality', 'city', 'state' ,'zip_code']
        labels = {'customer_name':'Full Name ','area_locality':'Address '}
        widgets = {'customer_name':forms.TextInput(attrs={'class':'form-control'}),'mobile_number':forms.NumberInput(attrs={'class':'form-control','max_length':'10'}),'area_locality':forms.TextInput(attrs={'class':'form-control'}), 'city':forms.TextInput(attrs={'class':'form-control'}), 'state':forms.TextInput(attrs={'class':'form-control'}),'zip_code':forms.NumberInput(attrs={'class':'form-control'})}

class Contact(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['customer_name', 'customer_email','mobile_number', 'query']
        labels = {'customer_name':'Name','customer_email':'Email'}
        widgets = {'customer_name':forms.TextInput(attrs={'class':'form-control','label_sufix':'+'}),'mobile_number':forms.NumberInput(attrs={'class':'form-control','max_length':'10'}), 'customer_email':forms.EmailInput(attrs={'class':'form-control'}), 'query':forms.Textarea(attrs={'class':'form-control'})}

class PaymentForm(forms.Form):
    amount = forms.FloatField()
    currency = forms.CharField(max_length=3)
    order_id = forms.CharField(max_length=32)
    receipt = forms.CharField(max_length=32)
    payment_capture = forms.IntegerField()

