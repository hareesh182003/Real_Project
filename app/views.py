from django.shortcuts import render
from app.forms import *
from app.models import *
from django.http import HttpResponse
# Create your views here.


def registration(request):
    EUFO = UserForm()
    EPFO = ProfileForm()
    d = {'EUFO':EUFO,'EPFO':EPFO}
    if request.method == 'POST' and request.FILES:
        NMUFO = UserForm(request.POST)
        NMPFO = ProfileForm(request.POST,request.FILES)
        if NMUFO.is_valid() and NMPFO.is_valid():

            MUFO = NMUFO.save(commit=False)
            pwd = NMUFO.cleaned_data['password']
            MUFO.set_password(pwd)
            MUFO.save()

            MPFO = NMPFO.save(commit=False)
            MPFO.username = MUFO
            MPFO.save()

            return HttpResponse('Sucessful')
        else:
            return HttpResponse('Invalid')
        





    

    return render(request,'registration.html',d)