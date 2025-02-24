from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from todo import models
from todo.models import ToDoo
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
 

def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')
        print(fnm,email,pwd)
        my_user = User.objects.create_user(fnm,email,pwd)
        my_user.save()
        return redirect('/login')
    return render(request, 'signup.html')


def user_login(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
        print(fnm,pwd)
        user1 = authenticate(request,username=fnm,password=pwd)
        if user1 is not None:
            login(request,user1)
            return redirect('/todo')
        else:
            return redirect('/login/')

    return render(request, 'login.html')


@login_required(login_url='/login')
def Todo(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        print(task)
        obj1 = ToDoo(title=task,User=request.user)
        obj1.save()
        return redirect('/todo')
    res = models.ToDoo.objects.filter(User=request.user).order_by('sr_no')
    for index, task in enumerate(res, start=1):
        task.serial_number = index  
    return render(request,'todo.html', {'res':res})


@login_required(login_url='/login')
def edit_todo(request, sr_no):
    user = request.user
    obj1 = get_object_or_404(ToDoo, sr_no=sr_no, User=user)  # Securely fetch the task

    if request.method == 'POST':
        task = request.POST.get('task')
        print(f"Updated Task: {task}")  # Debugging Output

        obj1.title = task
        obj1.save()

        return redirect('/todo')  # Redirect to the main task list

    return render(request, 'edit_todo.html', {'task': obj1})


@login_required(login_url='/login')
def delete_todo(request,sr_no):
    user = request.user
    todo = get_object_or_404(ToDoo, sr_no=sr_no, User=user)  # Securely fetch the task
    
    todo.delete()  # Optional: Add a success message

    return redirect('/todo')

def signout(request):
    logout(request)
    return redirect('/login')
