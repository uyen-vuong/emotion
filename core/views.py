from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.
def error404(request,*args, **kwargs):
    return render(request, "errors/404.html", {})

def sign_in(request,*args, **kwargs):
    return render(request, "sign-in.html", {})

def sign_up(request,*args, **kwargs):

    if request.method == 'GET':
        return render(request, "sign-up.html", {})
    else:
        return redirect('/error404')