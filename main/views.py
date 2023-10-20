from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .models import *
# Create your views here.

@login_required
def home(request):
    person = Individual.objects.get(user=request.user)
    partnerships = Patnership.objects.filter(owner=person).order_by('-amount')
    total = 0
    for ship in partnerships:
        total += ship.amount
    percentage_complete = round((total / person.main_target) * 100)
    left = person.main_target - total
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
    partnerships = Patnership.objects.filter(owner=person)
    try:
        partnerships = partnerships[:3]
    except:
        pass

    
    targets = TargetIndividual.objects.filter(owner=person).order_by('-created_at')
    try:
        targets = targets[:3]
    except:
        pass
    print(targets)
    return render(request, 'index.html', {'person': person, 'percent': percentage_complete, 'left': left, 'position': rs, 'partnerships': partnerships, 'targets': targets})


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
                    return redirect("main:home")
                else:
                    messages.error(request,"Invalid username or password.")
            else:
                messages.error(request,"Invalid username or password.")
    else:
        return redirect("main:home")
    form = AuthenticationForm()
    return render(request, 'login.html', {})