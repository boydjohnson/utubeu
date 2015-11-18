from django.shortcuts import render, redirect
from django.template.context import RequestContext

from django.contrib.auth.views import logout as auth_logout

# Create your views here.


def login(request):
    if request.method == 'GET':
        context = RequestContext(request, {'user': request.user})
        return render(request, 'login.html', context=context)



def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')