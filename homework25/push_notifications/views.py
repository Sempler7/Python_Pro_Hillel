from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    """Відображає головну сторінку чату"""
    return render(request, 'push_notifications/chat.html')