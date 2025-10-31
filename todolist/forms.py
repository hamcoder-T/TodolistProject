from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=250, required=True, label='Username', widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter your username'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(required=True, label="رمز عبور", widget=forms.PasswordInput(
        attrs={'placeholder': 'enter your password', 'class': 'form-control'}))
    confirm_password = forms.CharField(required=True, label="تایید رمز عبور", widget=forms.PasswordInput(attrs={
        'placeholder': 'confirm you password', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'enter a unique username for yourself',
                                               'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'enter your first name', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'enter your last name', 'class': 'form-control'}),
            'email': forms.TextInput(attrs={'placeholder': 'enter your email', 'class': 'form-control'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if username:
            if self.instance and hasattr(self.instance, 'pk'):
                if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
                    raise forms.ValidationError('username already exists!')
            elif User.objects.filter(username=username).exists():
                raise forms.ValidationError('username already exists!')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('password and its repeat dos\'nt same')
        return cleaned_data


class AddEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'begin', 'end']
        widgets = {
            'begin': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'is_done']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'عنوان وظیفه...', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'توضیحات...', 'class': 'form-control'}),
            'is_done': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)
