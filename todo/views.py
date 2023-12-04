from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

from .forms import TodoForm
# Create your views here.


def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    
    if request.method == 'GET':    
        return render(request, "todo/loginuser.html", {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, "todo/loginuser.html", {'form': AuthenticationForm(),'error': 'Имя или пароль введены не верно.'})
        else:
            login(request, user)
            return redirect('currenttodos')
        
        
def loginuser(request): 
    if request.method == 'GET':    
        return render(request, "todo/signupuser.html", {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
                
            except IntegrityError:
                return render(request, "todo/signupuser.html", {'form': UserCreationForm(), 'error': 'Пользователь с таким именем уже используется'} )    
        else:
            return render (
                request, 
                "todo/signupuser.html", 
                {'form': UserCreationForm(), 'error': 'Пароли не совпадают'}
                )

    
    
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    
def createtodo(request):
    if request.method == 'GET':
        return render(request, "todo/createtodo.html", {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect ('currenttodos')
        except ValueError:
            return render(request, "todo/createtodo.html", {'form': TodoForm(), 'error':'Переданы не верные данные, попробуйте еще раз'})
def currenttodos(request):
    return render(request, 'todo/currenttodos.html')    
    
    