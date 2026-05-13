from typing import List, Dict
from django.http import HttpRequest

from ninja import NinjaAPI
from ninja.errors import HttpError

from .models import Tag, Post, Comment
from .schemas import TagIn, TagOut, PostIn, PostOut, CommentIn, CommentOut
from task_manager.auth import AuthBearer

api = NinjaAPI(auth=AuthBearer(), urls_namespace="blog")


@api.post("/tags", response=TagOut)
def create_tag(request: HttpRequest, payload: TagIn) -> Tag:
    """Створює новий тег"""
    tag = Tag.objects.create(**payload.dict())
    return tag


@api.get("/tags", response=List[TagOut])
def list_tags(request: HttpRequest) -> List[Tag]:
    """Повертає список всіх тегів"""
    return list(Tag.objects.all())


@api.delete("/tags/{tag_id}")
def delete_tag(request: HttpRequest, tag_id: int) -> Dict[str, bool]:
    """Видаляє тег за його ідентифікатором"""
    try:
        tag = Tag.objects.get(id=tag_id)
    except Tag.DoesNotExist:
        raise HttpError(404, "Тег не знайдено")
    tag.delete()
    return {"success": True}


@api.post("/posts", response=PostOut)
def create_post(request: HttpRequest, payload: PostIn) -> Post:
    """Створює новий пост від імені авторизованого користувача"""
    data = payload.dict()
    tag_ids = data.pop("tag_ids")
    post = Post.objects.create(author=request.user, **data)
    post.tags.set(tag_ids)
    return post


@api.get("/posts", response=List[PostOut])
def list_posts(request: HttpRequest) -> List[Post]:
    """Повертає список всіх постів з тегами та коментарями"""
    return list(Post.objects.prefetch_related('tags', 'comments').all())


@api.get("/posts/{post_id}", response=PostOut)
def get_post(request: HttpRequest, post_id: int) -> Post:
    """Повертає пост за його ідентифікатором"""
    try:
        return Post.objects.prefetch_related('tags', 'comments').get(id=post_id)
    except Post.DoesNotExist:
        raise HttpError(404, "Пост не знайдено")


@api.put("/posts/{post_id}", response=PostOut)
def update_post(request: HttpRequest, post_id: int, payload: PostIn) -> Post:
    """Оновлює пост. Доступно тільки автору посту"""
    try:
        post = Post.objects.get(id=post_id, author=request.user)
    except Post.DoesNotExist:
        raise HttpError(404, "Пост не знайдено або немає доступу")

    data = payload.dict()
    tag_ids = data.pop("tag_ids")

    for attr, value in data.items():
        setattr(post, attr, value)

    post.save()
    post.tags.set(tag_ids)
    return post


@api.delete("/posts/{post_id}")
def delete_post(request: HttpRequest, post_id: int) -> Dict[str, bool]:
    """Видаляє пост. Доступно тільки автору посту"""
    try:
        post = Post.objects.get(id=post_id, author=request.user)
    except Post.DoesNotExist:
        raise HttpError(404, "Пост не знайдено або немає доступу")

    post.delete()
    return {"success": True}


@api.post("/posts/{post_id}/comments", response=CommentOut)
def add_comment(request: HttpRequest, post_id: int, payload: CommentIn) -> Comment:
    """Додає коментар до посту від імені авторизованого користувача"""
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise HttpError(404, "Пост не знайдено")

    comment = Comment.objects.create(post=post, author=request.user, **payload.dict())
    return comment


@api.get("/posts/{post_id}/comments", response=List[CommentOut])
def list_comments(request: HttpRequest, post_id: int) -> List[Comment]:
    """Повертає список всіх коментарів до посту"""
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise HttpError(404, "Пост не знайдено")

    return list(post.comments.all())


@api.delete("/posts/{post_id}/comments/{comment_id}")
def delete_comment(request: HttpRequest, post_id: int, comment_id: int) -> Dict[str, bool]:
    """Видаляє коментар. Доступно тільки автору коментаря"""
    try:
        comment = Comment.objects.get(id=comment_id, post_id=post_id, author=request.user)
    except Comment.DoesNotExist:
        raise HttpError(404, "Коментар не знайдено або немає доступу")

    comment.delete()
    return {"success": True}
