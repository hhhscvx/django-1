from django import template
from ..models import Post
from django.db.models import Count

register = template.Library()


@register.simple_tag  # регистрирует функцию как простой тег шаблона
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=3):  # Последние count постов
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}  # отправляем данную хуйнюшку на latest_posts.html, как в render`е


@register.simple_tag
def get_most_commented_posts(count=3):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).exclude(total_comments=0).order_by('-total_comments')[:count]
