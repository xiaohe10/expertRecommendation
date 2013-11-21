# Create your views here.
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response

def list_experts(request):
    if request.user.is_authenticated():
        user = request.user
        return render_to_response('expert/list_experts.html',locals())
    else:
        return HttpResponseRedirect("/")