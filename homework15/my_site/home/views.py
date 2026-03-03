from django.http import HttpResponse
from django.shortcuts import render

def home_view(request):
    return HttpResponse("Ласкаво просимо на головну сторінку.")

def about_view(request):
    return HttpResponse("Сторінка про нас.")

def contact_view(request):
    return HttpResponse("Зв'яжіться з нами.")

def post_view(request, id):
    return HttpResponse(f"Ви переглядаєте пост з ID: {id}")

def profile_view(request, username):
    return HttpResponse(f"Ви переглядаєте профіль користувача: {username}")

def event_view(request, year, month, day):
    return HttpResponse(f"Дата події: {year}-{month}-{day}")

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def post(request):
    return render(request, 'post.html')

def profile(request):
    return render(request, 'profile.html')

def event(request):
    return render(request, 'event.html')



