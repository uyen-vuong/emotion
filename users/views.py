# from asyncio import FastChildWatcher
# from multiprocessing import context
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_out
# from django.contrib.auth.password_validation import validate_password
# from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.http import HttpResponse
from users.forms import LoginForm, CustomUserCreationForm
# Create your views here.
def register(request):
    if request.method == "POST":
        # create a new account 
        form_  = CustomUserCreationForm(request.POST)
        if form_.is_valid():  
            user = form_.save()
            messages.success(request, 'Account created successfully: {}'.format(user.fullname))  
            context = {'status': True}
        else:  
            # form = CustomUserCreationForm()  
            messages.error(request, 'Can not create account. Email is exsited!')  
            context = {'status': False}
        return render(request, 'sign-up.html', context)

def login_view(request):
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            # login & redirect
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)  
                    """
                    Here if the remember me is False, that is why expiry is set to 0 seconds. 
                    So it will automatically close the session after the browser is closed.
                    """
                return redirect('manager:dashboard')
            else:
                messages.info(request, 'Invalid Username or Password')
            context = {'status' : False}
            return render(request, 'sign-in.html', context)
        else:
            messages.info(request, 'Can not login right now!')
            context = {'status' : False}
            return render(request, 'sign-in.html', context) 
    else:
        messages.info(request, 'Sucessful log out!')
        context = {'status' : True}
        return render(request, 'sign-in.html', context) 

@login_required
def logout_view(request):
    """
    Removes the authenticated user's ID from the request and flushes their
    session data.
    """
    user = getattr(request, 'user', None)
    if hasattr(user, 'is_authenticated') and not user.is_authenticated():
        user = None
    user_logged_out.send(sender=user.__class__, request=request, user=user)

    request.session.flush()
    if hasattr(request, 'user'):
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()
    # Dispatch the signal before the user is logged out so the receivers have a
    # chance to find out *who* logged out.
    logout(request)
    list(messages.get_messages(request))
    return HttpResponseRedirect('/')

@login_required
def profile(request):
    if request.method == 'GET':
        return render(request, "profile.html", {})