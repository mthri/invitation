from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# @method_decorator(login_required, name='dispatch')
@login_required
def index(request):
    return render(request, 'dashboard/base.html')

def profile(request):
    return render(request, 'dashboard/profile.html', context={'user': request.user})
