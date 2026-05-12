from django.contrib import admin
from .models import Category, Ad, Comment, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "location", "birth_date")
    search_fields = ("user__username", "location")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "is_active", "category", "user", "created_at")
    list_filter = ("category", "is_active")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("content", "ad", "user", "created_at")

