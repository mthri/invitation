from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import View

from .mixins import PremissionMixin
from .forms import UserForm

@login_required
def index(request):
    return render(request, 'dashboard/base.html')
    
class Profile(PremissionMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/profile.html', 
                      context={'user': request.user})
    
    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST, instance=self.request.user)
        if form.is_valid():
            form.save()

        return render(request, 'dashboard/profile.html', 
                      context={'user': request.user,
                               'errors': form.errors.get_json_data()})
