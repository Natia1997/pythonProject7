from django.shortcuts import render
from . models import Room, Meal,Comment
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from .form import MealForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q


def home(request):
        room = Room.objects.get(id=int(pk))
        room_meals = room.meal_set.all()
        context = {'room': room, 'room_meals': room_meals}
        return render(request, 'base/rooms.html', context)


def room(request, pk):
        room = Room.objects.get(id=int(pk))
        room_meals = room.meal_set.all()
        context = {'room': room, 'room_meals': room_meals}
        return render(request, 'base/rooms.html', context)


@login_required(login_url='login')
def add_meal_to_room(request, pk):
    room = Room.objects.get(id=int(pk))

    if request.method == 'POST':
        form = MealForm(request.POST, request.FILES)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.room = room

            meal.save()

            return redirect('room', pk=room.id)

    else:
        form = MealForm()

    return render(request, 'base/add_meal_to_room.html', {'room': room, 'form': form} )

@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'obj': room}
    if request.user != room.host:
        return HttpResponse("<h1>You don't have permission!</h1>")
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context)

def login_page(request):
    page = "login"
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User doesn't exist!")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Password is incorrect!")
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')

def register_page(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
    return render(request, 'base/login_register.html', {'form': form})

@login_required(login_url='login')
def delete_meal(request, pk):
    meal = get_object_or_404(Meal, id=pk)
    if request.method == "POST":
        if request.META.get('HTTP_REFERER') and 'add_meal_to_room' in request.META.get('HTTP_REFERER'):

            pass
        meal.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': meal})
def meal_info(request, pk):
    meal = Meal.objects.get(id=int(pk))

    return render(request, 'base/meal_info.html', {'meal': meal})



