from django.shortcuts import render

# Create your views here.
def myadmin(request):
    return render(request,'myadmin/admin_panel.html')