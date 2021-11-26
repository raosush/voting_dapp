from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
import csv
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings

from authentication.models import User
import requests
import string
import random

class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CsvImportForm(forms.Form):
    csv_file = forms.FileField(
        label='Upload a CSV to bulk import users', widget=widgets.FileInput)

    def save(self):
        file_data = self.cleaned_data["csv_file"].read().decode(
            'utf-8').split("\n")
        try:
            with transaction.atomic():
                for line in csv.reader(file_data):
                    if len(line) == 2:
                        characters = string.ascii_letters + string.digits + string.punctuation
                        password = ''.join(random.choice(characters) for _ in range(12))
                        form = UserCreationForm(data={'email': line[0], 'username': line[1], 'password1': password, 'password2': password})
                        form.save()
                        send_mail(subject='Voting Dapp - New Account',
                         message='A new account has been created for your email. Credentials are as follows:\nUsername: %s\nPassword: %s' %(line[1], password),
                         from_email=settings.EMAIL_HOST_USER, recipient_list=[line[0]])
                    else:
                        raise ValidationError(message='Incorrect CSV file/format')
        except ValidationError as e:
            transaction.rollback()
            raise e

class RESTApiImportForm(forms.Form):
    rest_url = forms.URLField(label='Enter a REST API URL', widget=widgets.URLInput)

    def save(self):
        rest_url = self.cleaned_data['rest_url']
        response = requests.get(rest_url)
        body = []
        if response.status_code == 200:
            body = response.json()
        try:
            with transaction.atomic():
                for b in body:
                    if len(b) == 2:
                        characters = string.ascii_letters + string.digits + string.punctuation
                        password = ''.join(random.choice(characters) for _ in range(12))
                        form = UserCreationForm(data={'email': b[0], 'username': b[1], 'password1': password, 'password2': password})
                        form.save()
                        send_mail(subject='Voting Dapp - New Account',
                         message='A new account has been created for your email. Credentials are as follows:\nUsername: %s\nPassword: %s' %(b[1], password),
                         from_email=settings.EMAIL_HOST_USER, recipient_list=[b[0]])
                    else:
                        raise ValidationError(message='Incorrect CSV file/format')
        except ValidationError as e:
            transaction.rollback()
            raise e
