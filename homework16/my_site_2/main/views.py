from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from datetime import datetime
from .forms import ContactForm


def home(request):
    return render(request, 'main/home.html', {'title': 'Головна'})


def about(request):
    context = {
        'title': 'Про нас',
        'company_description': 'Наша компанія займається розробкою програмного забезпечення та допомагає клієнтам досягати успіху.',
        'updated_at': datetime.now(),
    }
    return render(request, 'main/about.html', context)


class ContactView(View):
    def get(self, request):
        form = ContactForm()
        context = {
            'title': 'Контакти',
            'form': form,
            'address': 'м. Київ, вул. Хрещатик, 1',
            'phone': '+380 67 123 45 67',
            'email': 'info@example.com',
        }
        return render(request, 'main/contact.html', {'form': form, 'title': 'Контакти'})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # після відправки повертаємо на головну
        return render(request, 'main/contact.html', {'form': form, 'title': 'Контакти'})

class ServiceView(View):
    services = [
        {'name': 'Розробка сайтів', 'description': 'Створення сучасних веб-рішень', 'category': 'web'},
        {'name': 'Мобільні додатки', 'description': 'Розробка додатків для iOS та Android', 'category': 'mobile'},
        {'name': 'Консалтинг', 'description': 'Допомога у виборі технологій та архітектури', 'category': 'consulting'},
        {'name': 'Технічна підтримка', 'description': 'Супровід та підтримка клієнтів', 'category': 'support'},
    ]

    def get(self, request):
        query = request.GET.get('q')
        category = request.GET.get('category')

        filtered_services = self.services

        if query:
            filtered_services = [
                s for s in filtered_services
                if query.lower() in s["name"].lower() or query.lower() in s["description"].lower()
            ]

        if category:
            filtered_services = [s for s in filtered_services if s["category"] == category]

        context = {
            'title': 'Послуги',
            'services': filtered_services
        }
        return render(request, 'main/services.html', context)



class HelloView(View):
    def get(self, request):
        return render(request, 'main/home.html', {'username': 'username'})