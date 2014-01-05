#-*-coding:UTF-8-*-
# Create your views here.
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
@csrf_protect

def register(request):
    message=''
    if request.method == 'POST':
        validcode = request.POST['validcode']
        if(validcode != 'zhuanjiaku'):
            message = '验证码错误，应该是 zhuanjiaku'
            form = UserCreationForm(request.POST)
            return render(request,"account/register.html", {'form': form,'message':message})
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
        try:
            user = User.objects.get(username = request.POST['username'])
            message = "该用户名已经存在"
        except:
            pass1 = request.POST["password1"]
            pass2 = request.POST["password2"]
            if pass1 != pass2:
                message = "密码输入不一致"
            elif  pass1 == '':
                message = "密码不能为空"

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
        return HttpResponseRedirect("/experts/list/1/")
    if request.method == 'POST':
        username = request.POST.get('username', '')
        print username
        password = request.POST.get('password', '')
        print password
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect("/experts/list/1/")
        else:
            # Show an error page
            return render(request,"account/login.html",{'message':'用户名或密码错误'})
    else:
        return render(request,"account/login.html")
