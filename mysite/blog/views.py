from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, \
    PageNotAnInteger  # Pag позволяет осуществлять постраничную разбивку результатов, дальше импортируем ошибки


def post_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 3)  # разбивает список постов на страницы, содержащие по 3 поста каждая
    page_number = request.GET.get('page', 1)  # запрошенный номер страницы, если такой нет, то по умолчанию 1-ая стр.
    try:
        posts = paginator.page(page_number)  # получаем объект страницы с постами для указанного номера страницы
    except PageNotAnInteger:
        posts = paginator.page(1)  # Если не целое число, выдаем первую страницу
    except EmptyPage:
        # Если page_number вне диапазона, выдать ласт страницу
        posts = paginator.page(paginator.num_pages)  # num_pages = число страниц -> будет как ласт страница
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})
