import logging
from typing import Any, Dict

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, CreateView

from .forms import ArticleForm, CustomUserRegistrationForm
from .middleware import RequestCountMiddleware
from .models import Article

logger = logging.getLogger('custom_logger')


def home_view(request: HttpRequest) -> HttpResponse:
    """Перенаправляє користувача на список статей або сторінку входу"""
    if request.user.is_authenticated:
        return redirect('article-list')
    return redirect('login')


class ArticleListView(LoginRequiredMixin, ListView):
    """Представлення для відображення списку статей."""

    model = Article
    template_name = 'customization/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10
    login_url = 'login'

    def get_queryset(self) -> QuerySet[Article]:
        """Повертає список статей з фільтрацією за статусом і категорією"""
        queryset = Article.objects.with_related()

        status = self.request.GET.get('status')
        category_id = self.request.GET.get('category')

        if status == 'published':
            queryset = queryset.published()
        elif status == 'draft':
            queryset = queryset.drafts()

        if category_id:
            queryset = queryset.by_category(category_id)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Додає статистику категорій до контексту шаблону"""
        context = super().get_context_data(**kwargs)
        context['category_stats'] = Article.objects.category_statistics()
        return context


class ArticleDetailView(LoginRequiredMixin, DetailView):
    """Представлення для перегляду деталей статті."""

    model = Article
    template_name = 'customization/article_detail.html'
    context_object_name = 'article'
    login_url = 'login'

    def get_queryset(self) -> QuerySet[Article]:
        """Повертає оптимізований queryset статей"""
        return Article.objects.with_related()


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """Представлення для створення нової статті."""

    model = Article
    form_class = ArticleForm
    template_name = 'customization/article_form.html'
    login_url = 'login'

    def form_valid(self, form: ArticleForm) -> HttpResponse:
        """Зберігає статтю з поточним користувачем як автором"""
        form.instance.author = self.request.user

        color = form.cleaned_data.get('color')
        if color:
            metadata = form.instance.metadata or {}
            metadata['color'] = color
            form.instance.metadata = metadata

        article = super().form_valid(form)
        logger.info(f'Article created via web: {form.instance.title} by {self.request.user}')
        return article


def register_view(request: HttpRequest) -> HttpResponse:
    """Реєструє нового користувача або відображає форму реєстрації"""
    if request.user.is_authenticated:
        return redirect('article-list')

    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            logger.info(f'New user registered: {user.username}')
            return redirect('article-list')
        else:
            logger.warning('Invalid registration attempt')
    else:
        form = CustomUserRegistrationForm()

    return render(request, 'customization/register.html', {'form': form})


def metrics_view(request: HttpRequest) -> JsonResponse:
    """Повертає метрики кількості запитів до сервера"""
    return JsonResponse({
        'request_count': RequestCountMiddleware.request_count
    })