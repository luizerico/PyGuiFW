from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect

# Create your views here.

def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        #return HttpResponseRedirect("/apprisk/filter/list/")
    else:
        return HttpResponseRedirect("/apprisk/login")


def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect("/apprisk/login")


def denied_view(request):
    context = {'connections': 'processes'}
    return render(request, 'denied.html', context)