from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, \
    PageNotAnInteger  # Pag позволяет осуществлять постраничную разбивку результатов, дальше импортируем ошибки
from django.views.generic import ListView
from .forms import EmailPostForm


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


def post_share(request, post_id):  # запрос и id поста
    # Извлечь пост по id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)  # извлечегие из БД поста по id и published
    if request.method == 'POST':  # POST -> форма отправлена на обработку
        form = EmailPostForm(request.POST)  # обработка данных, введенных пользователем
        if form.is_valid():  # формы введены корректно
            cd = form.cleaned_data  # получение очищенных данных из формы (словарь полей формы и их значений)
            # ... отправить эл. письмо
    else:  # GET -> пользователь получил форму и должен ее заполнить -> она должна быть пустой
        form = EmailPostForm()
    return render(request,  # рендерит шаблон с передачей поста и экземпляра формы
                  'blog/post/share.html',
                  {'post': post, 'form': form})


class PostListView(ListView):
    """Альтернативное представление списка постов"""
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
