from django.shortcuts import render
from  accounts.models import Account,MyAccountManager
# Create your views here.
def myadmin(request):
    
    return render(request,'myadmin/admin_panel.html')


def user_management(request):
    return render(request,'myadmin/user_management.html')