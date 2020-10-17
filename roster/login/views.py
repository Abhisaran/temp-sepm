from django.http import HttpResponse
from .models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms


# Create your views here.
# from source.roster.apps.login import models


def index(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            # print(form.as_p())
            # print(form.cleaned_data['your_user_id'])
            # print(form.cleaned_data['your_password'])
            # print(form.cleaned_data['mode'])
            print("Hello at login form")
            return HttpResponseRedirect('/main/' + str(form.cleaned_data['your_user_id']) + '-' + str(
                form.cleaned_data['your_password']) + '-' + str(form.cleaned_data['mode']))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'login/index.html', context)


class LoginForm(forms.Form):
    mode_choice = [('staff', 'Staff'), ('manager', 'Manager'), ('admin', 'Admin')]
    your_user_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'field', 'id': 'user', 'placeholder': 'Username'}), label='',
        max_length=20)
    your_password = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'field', 'id': 'pass', 'placeholder': 'Password'}), label='',
        max_length=20)
    mode = forms.ChoiceField(label='', choices=mode_choice, widget=forms.Select(attrs={'class': 'field'}))
