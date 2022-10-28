
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.


def signup_user(request):
    if request.user.is_authenticated:
        return redirect(home_user)
    form=CreateUserForm()
    if request.method =='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            messages.success(request,'Account was created')
            return redirect('home')
    context={'form':form}
    return render(request,'home/signup.html',context)





def login_user(request):
    if request.user.is_authenticated:
        return redirect(home_user)
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            if user.is_superuser is False:
                login(request,user)
                return redirect(home_user)
            else:
                return redirect('admin_login')
        else:
            messages.info(request,'Username or Password is Incorrect')
            return render(request,'home/login.html')
    return render(request,'home/login.html')





def home_user(request):
    if request.user.is_superuser:
        return redirect('admin_home')
    if request.user.is_authenticated:
        return render(request,'home/home.html')
    return redirect(login_user)



def logout_user(request):
    logout(request)
    return redirect('login')





def admin_login(request):
    if request.user.is_superuser:
        return redirect('admin_home')
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            if user.is_superuser:
                login(request,user)     
                return redirect(admin_home)
            else:
                return redirect('login')
        else:
            messages.info(request,'Username or Password is Incorrect')
            return render(request,'home/admin_login.html')
    return render(request,'home/admin_login.html')




@login_required(login_url='admin_login')
def admin_home(request):
    if request.user.is_superuser:
        data=User.objects.all()
        context={'data':data}
        return render(request,'home/admin_home.html',context)
    return redirect('admin_login')


def logout_admin(request):
        logout(request)
        return redirect('admin_login')


def admin_delete(request,id):
    user=User.objects.get(pk=id)
    user.delete()
    return HttpResponseRedirect(reverse('admin_home'))

def insert_user(request,id=0):
    form=CreateUserForm()
    if request.user.is_superuser:
        if request.method =='GET':
            if id==0:
                form = CreateUserForm(request.POST)
            else:
                user=User.objects.get(pk=id)
                form = CreateUserForm(instance=user)
            return render(request,'home/user_insert.html',{'form':form})
        else:
            if id==0:
                form = CreateUserForm(request.POST)
            else:
                user=User.objects.get(pk=id)
                form = CreateUserForm(request.POST,instance=user)
            if form.is_valid():
                form.save()
            return redirect('admin_home')
    return render(request,'home/admin_login.html')
    


def search(request):
    if request.user.is_superuser:
        query=request.GET['q']
        data=User.objects.filter(username__icontains=query)
        context={'data':data}
        return render(request,'home/admin_search.html',context)