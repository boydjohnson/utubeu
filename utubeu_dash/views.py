from django.shortcuts import render
from django.core.exceptions import PermissionDenied


def dashboard(request):
    if request.method == 'GET':
        user = request.user
        return render(request, 'utubeu-dash/dash.html', context={'user': user})
    else:
        raise PermissionDenied("Method not supported.")