from ast import UAdd
from turtle import up
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, "acc/index.html")

def login_user(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        pw = request.POST.get("upass")
        user = authenticate(username=un, password=pw)
        if user:
            login(request, user)
            messages.success(request, f": {user}님 환영합니다! :)")
            return redirect("acc:index")
        else:
            messages.error(request,": LOGIN FAIL")
    return render(request, "acc/login.html")

def logout_user(request):
    logout(request)
    return redirect('acc:login')

from .models import User
def signup(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        up = request.POST.get("upass")
        ua = request.POST.get("uage")
        ut = request.POST.get("utext")
        upic = request.FILES.get("upic")
        
        try:          
            User.objects.create_user(username = un, password = up, comment = ut, age = ua, pic = upic)
        except:
            messages.error(request,f"{un} 이미 존재합니다.")
        return redirect("acc:login")
    return render(request,"acc/signup.html")

def profile(request):
    return render(request,'acc/profile.html')

from django.contrib.auth.hashers import check_password
def delete(request):
    ck = request.POST.get("ckpw")
    if check_password(ck, request.user.password):
        print("1222345")
        # request.user.pic.delete()
        # request.user.delete()
        return redirect('acc:index')
    else:
        pass #19일
    return redirect('acc:profile')


def usermod(request):
    if request.method =="POST":
        u = request.user
        un = request.POST.get("uname")
        up = request.POST.get("upass")
        uc = request.POST.get("utext")
        ua = request.POST.get("uage")
        upic = request.FILES.get("upic")

        if up:
            u.set_password(up)

        if upic:
            request.user.pic.delete()
            u.pic = upic
        u.username = un
        u.comment = uc
        u.age = ua
        u.save()
        login(request,u)
        return redirect("acc:profile")

    return render(request,'acc/update.html')
