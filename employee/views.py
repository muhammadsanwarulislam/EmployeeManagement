from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import UserForm


def user_login(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if request.GET.get('next', None):
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            context["error"] = "Provide valid credentials !!"
            return render(request, "auth/login.html", context)
    else:
        return render(request, "auth/login.html", context)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_page'))

@login_required(login_url='/login/')
def success(request):
    context = {}
    context['user']=request.user
    template_name='auth/success.html'
    return render(request,template_name,context)

@login_required(login_url='/login/')
def employee_list(request):
    context = { }
    users            = User.objects.all()
    context['title'] = 'Employee'
    context['users'] = users
    template_name    = 'employee/employee_list.html'
    return render(request,template_name,context)

@login_required(login_url='/login/')
def employee_detalis(request,id=None):
    context = { }
    user    = get_object_or_404(User,id=id)
    context['user'] = user
    template_name   = 'employee/employee_details.html'
    return render(request,template_name,context)

@login_required(login_url='/login/')
def employee_add(request):
    context = { }
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            template_name = 'employee/employee_add.html'
            context['user_form'] = user_form
            return render(request,template_name,context)
    else:
        user_form = UserForm()
        template_name = 'employee/employee_add.html'
        context['user_form'] = user_form
        return render(request,template_name,context)

@login_required(login_url='/login/')
def employee_edit(request,id=None):
    context = {}
    user = get_object_or_404(User,id=id)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            template_name = 'employee/employee_edit.html'
            context['user_form'] = user_form
            return render(request,template_name,context)
    else:
        user_form = UserForm(instance=user)
        template_name = 'employee/employee_edit.html'
        context['user_form'] = user_form
        return render(request,template_name,context)

@login_required(login_url='/login/')
def employee_delete(request,id = None):
    user = get_object_or_404(User,id=id)
    if request.method=='POST':
        user.delete()
        return HttpResponseRedirect(reverse('employee_list'))
    else:
        context={}
        context['user'] = user
        template_name ='employee/employee_delete.html'
        return render(request,template_name,context) 
