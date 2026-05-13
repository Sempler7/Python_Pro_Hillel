from django.urls import path
from django.contrib.auth import views as auth_views
from .views import ArticleDetailView, ArticleCreateView, register_view, home_view, ArticleListView, metrics_view
from .api_views import ArticleListCreateAPIView, ArticleRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', home_view, name='home'),
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('article/create/', ArticleCreateView.as_view(), name='article-create'),
    path('api/articles/', ArticleListCreateAPIView.as_view(), name='api-article-list'),
    path('api/articles/<int:pk>/', ArticleRetrieveUpdateDestroyAPIView.as_view(), name='api-article-detail'),
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='customization/login.html'), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('metrics/', metrics_view, name='metrics'),
]
