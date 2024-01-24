from django.shortcuts import render

# Create your views here.
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def registration(request):
    ufo=UserForm()
    pfo=ProfileForm()

    d={'ufo':ufo,'pfo':pfo}

    if request.method=='POST' and request.FILES:
        ufd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)

        if ufd.is_valid() and pfd.is_valid():
            MUFDO=ufd.save(commit=False)
            pw=ufd.cleaned_data['password']

            MUFDO.set_password(pw)
            MUFDO.save()

            MPFDO=pfd.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()

            send_mail('Registration Successful',
                      'Thank You For Registering With Us.After Verification we will Contact You Soon.',
                      'arijitswain8000@gmail.com',
                      [MUFDO.email],
                      fail_silently=False)

            return HttpResponse('Registration Sucessful')
        else:
            return HttpResponse('Invalid Input')
    return render(request,'registration.html',d)


def home(request):
    if request.session.get('username'):
        Username=request.session.get('username')
        d={'Username':Username}
        return render(request,'home.html',d)

    return render(request,'home.html')

def user_login(request):
    if request.method=="POST":
        Username=request.POST['un']
        Password=request.POST['pw']

        AUO=authenticate(username=Username,password=Password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=Username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid Credntial')
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def profile_display(request):
    un=request.session.get('username')
    UO=User.objects.get(username=un)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'profile_display.html',d)
