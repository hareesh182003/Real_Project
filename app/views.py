from django.shortcuts import render
from app.forms import *
from app.models import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
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

            send_mail('Project Registration',
                    'Thanks For Your Response',
                    'hareeshgarisha@gmail.com',
                    [MUFO.email],
                    fail_silently=True)

            return HttpResponse('Sucessful')
        else:
            return HttpResponse('Invalid')
        
    return render(request,'registration.html',d)

def home(request):
    if request.session.get('username'):
        username = request.session.get('username')
        d = {'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        passw = request.POST['password']
        AUO = authenticate(username = username,password = passw)
        if AUO:
            if AUO.is_active:
                login(request,AUO)
                request.session['username'] = username
                return HttpResponseRedirect(reverse('home'))
                
            else:
                return HttpResponse('Not active user')
        else:
            return HttpResponse('Invalid Credentials')
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return  HttpResponseRedirect(reverse('home'))
@login_required
def profile_page(request):
    username = request.session.get('username')
    UO = User.objects.get(username=username)
    PO = Profile.objects.get(username=UO)
    d = {'UO':UO,'PO':PO}
    return render(request,'profile_page.html',d)
@login_required
def change_password(request):
    if request.method == 'POST':
        pwd = request.POST['pwd']
        rpwd = request.POST['rpwd']
        username = request.session.get('username')
        if pwd == rpwd:
            UO = User.objects.get(username=username)
            UO.set_password(pwd)
            UO.save()
            return HttpResponse('Password Changed Successfully')
        else:
            return HttpResponse('The password not matched')
    return render(request,'change_password.html')

def reset_password(request):
    if request.method == 'POST':
        user = request.POST['user']
        pwd = request.POST['pwd']
        rpwd = request.POST['rpwd']

        if pwd == rpwd:
            UO = User.objects.filter(username=user)
            if UO:
                UO[0].set_password(pwd)
                UO[0].save()
                return render(request,'user_login.html')
            else:
                return HttpResponse('Not a valid user')
        else:
            return HttpResponse('The password not matched')
    return render(request,'reset_password.html')