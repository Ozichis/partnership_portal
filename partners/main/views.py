from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .models import *
from .forms import ChurchTargetForm

from rest_framework import status
# Create your views here.

@login_required
def slash(request):
    if request.user.user_type == 1:
        return redirect("main:home_church")
    elif request.user.user_type == 2:
        return redirect("main:home")
    else:
        return redirect("/admin/")

@login_required
def church_partnerships(request):
    church = Church.objects.get(userinfo=request.user)
    members = Individual.objects.filter(church=church)
    arms = PatnershipArm.objects.all()
    partnerships = Patnership.objects.filter(owner__church=church).order_by('-date_payed')
    return render(request, "Church-Partnerships.html", {"partnerships": partnerships, "members": members, "arms": arms})    


@login_required
def church_targets(request):
    church = Church.objects.get(userinfo=request.user)
    members = Individual.objects.filter(church=church)
    arms = PatnershipArm.objects.all()
    church = Church.objects.get(userinfo=request.user)
    partnerships = TargetChurch.objects.filter(owner=church).order_by('-created_at')
    return render(request, "Church-Targets.html", {"targets": partnerships, "members": members, "arms": arms})    

@login_required
def home_church(request):
    church = Church.objects.get(userinfo=request.user)
    partnerships = Patnership.objects.filter(owner__church=church).order_by('-date_payed')
    total = 0
    for ship in partnerships:
        total += ship.amount
    percentage_complete = round((total / church.main_target) * 100)
    percentage_complete = 100 if percentage_complete > 100 else percentage_complete
    left = church.main_target - total
    left = 0 if left < 0 else left

    try:
        partnerships = partnerships[:3]
    except:
        pass

    members = Individual.objects.filter(church=church)
    arms = PatnershipArm.objects.all()
    
    targets = TargetChurch.objects.filter(owner=church).order_by('-created_at')
    try:
        targets = targets[:3]
    except:
        pass

    return render(request, "church_admin_1.html", {'left': left, 'members': members, 'arms': arms, 'percent': percentage_complete, 'partnerships': partnerships, 'targets':  targets, 'church': church, 'admin': request.user}, status=200)

@login_required
def home(request):
    person = Individual.objects.get(user=request.user)
    partnerships = Patnership.objects.filter(owner=person).order_by('-amount')
    total = 0
    for ship in partnerships:
        total += ship.amount
    percentage_complete = round((total / person.main_target) * 100)
    percentage_complete = 100 if percentage_complete > 100 else percentage_complete
    left = person.main_target - total
    left = 0 if left < 0 else left
    partners = Individual.objects.filter(church=person.church)
    all_details = {}
    for partner in partners:
        all_details[partner.name] = 0
        partnerships = Patnership.objects.filter(owner=partner)
        for ship in partnerships:
            all_details[partner.name] += ship.amount
    all_details = reversed(sorted(all_details.items(), key=lambda x:x[1]))
    all_details = dict(all_details)
    rs = 1
    for key, value in all_details.items():
        if key == person.name:
            position = rs
            break
        else:
            rs += 1
    partnerships = Patnership.objects.filter(owner=person).order_by('-date_payed')
    try:
        partnerships = partnerships[:3]
    except:
        pass

    
    targets = TargetIndividual.objects.filter(owner=person).order_by('-created_at')
    try:
        targets = targets[:3]
    except:
        pass
    return render(request, 'index.html', {'person': person, 'percent': percentage_complete, 'left': left, 'position': rs, 'partnerships': partnerships, 'targets': targets})

def add_partnership(request):
    if request.method == "POST":
        if request.user.user_type == 1 or request.user_type == 2:
            instance = request.POST.copy()
            instance.pop('arm')
            instance.pop('owner')
            instance.pop('csrfmiddlewaretoken')
            instance.pop('recaptchaResponse')
            instance.pop('amount')
            Patnership.objects.create(amount=request.POST.get('amount'), owner=Individual.objects.get(name=request.POST.get('owner')), arm=PatnershipArm.objects.get(name=request.POST.get('arm')))
            messages.success(request, "Partnership has been added")
            print(request.META.get('HTTP_REFERER', '/'))
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request, "You do not have permission to add partnership")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect("main:home_church")

def delete_partnership(request, id):
    if request.method == "GET":
        if request.user.user_type == 1 or request.user.user_type == 2 or (Patnership.objects.get(id=id).owner__church_id == id):
            try:
                Patnership.objects.get(id=id).delete()
                print()
                messages.success(request, "Successful deletion")
            except:
                messages.error(request, "Specific partnership doesn't exist")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request, "You do not have permission to delete partnership")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def add_target(request):
    church = Church.objects.get(userinfo=request.user)
    instance = request.POST.copy()
    instance["owner"] = church
    if request.method == "POST":
        if request.user.user_type == 1 or request.user_type == 2:
            form = ChurchTargetForm(instance)
            if form.is_valid():
                form.save()
                messages.success(request, "Target has been added")
                return redirect(request.POST.get('next', '/church/'))
            messages.error(request, "There is an error with your submission")
            return HttpResponseRedirect(request.POST.get('next', '/church/'))
        else:
            messages.error(request, "You do not have permission to add church targets")
            return HttpResponseRedirect(request.POST.get('next', '/church/'))
    return redirect("main:home_church")

def delete_target(request, id):
    if request.method == "GET":
        if request.user.user_type == 1 or request.user.user_type == 2:
            try:
                TargetChurch.objects.get(id=id).delete()
                messages.success(request, "Successful deletion")
            except:
                messages.error(request, "Specific target doesn't exist")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request, "You do not have permission to delete targets")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def partnerships(request):
    person = Individual.objects.get(user=request.user)
    partnerships = Patnership.objects.filter(owner=person).order_by('-date_payed')
    return render(request, 'Partnerships.html', {'partnerships': partnerships})

def targets(request):
    person = Individual.objects.get(user=request.user)
    targets = TargetIndividual.objects.filter(owner=person, is_active=True).order_by('-created_at')
    return render(request, 'Targets.html', {'targets': targets})

def acc_logout(request):
    logout(request)
    return redirect('main:home')
def acc_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}.")
                    user = User.objects.get(username=username)
                    if user.user_type == 2:
                        return redirect("main:home")
                    elif user.user_type == 1:
                        return redirect("main:home_church")
                    return redirect("/admin/")
                else:
                    messages.error(request,"Invalid username or password.")
            else:
                messages.error(request,"Invalid username or password.")
    else:
        if request.user.user_type == 1:
            return redirect("main:home_church")
        if request.user.user_type == 2:
            return redirect("main:home")
        return redirect("/admin/")
    form = AuthenticationForm()
    return render(request, 'login.html', {}, status=200)