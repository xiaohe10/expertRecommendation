# Create your views here.
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
@csrf_protect

def register(request):
    if request.method == 'POST':
        validcode = request.POST['validcode']
        if(validcode != 'zhuanjiaku'):
            message = 'invalid code'
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request,"account/register.html", {
        'form': form,'message':message
    })


def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/")
@csrf_protect
def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/experts")
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect("/experts")
        else:
            # Show an error page
            return render(request,"account/login.html",{'message':'login fail'})
    else:
        return render(request,"account/login.html")