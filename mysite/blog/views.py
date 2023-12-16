from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)  # Извлекается Тег с переданным tag_slug
        post_list = post_list.filter(tags__in=[tag])
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
                  {'posts': posts,
                   'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(
        active=True)  # Я так понял тут мы обращаемся в ForeignKey модели comments -> фильтруем активные комментарии
    form = CommentForm()  # Форма для комментирования пользователем

    post_tags_ids = post.tags.values_list('id',
                                          flat=True)  # получаем кортежи тегов по id (flat чтобы не [(1,), (2,)..), а [1, 2..]
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(
        id=post.id)  # В опубликованных постах ищем посты с хоть одним таким же тегом, исключая сам пост
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[
                    :4]  # same tags считает кол-во одинаковых тегов и потом всё сортируется

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form,
                   'similar_posts': similar_posts})


def post_share(request, post_id):  # запрос и id поста
    # Извлечь пост по id
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)  # извлечегие из БД поста по id и published

    sent = False

    if request.method == 'POST':  # POST -> форма отправлена на обработку
        form = EmailPostForm(request.POST)  # обработка данных, введенных пользователем
        if form.is_valid():  # формы введены корректно
            cd = form.cleaned_data  # получение очищенных данных из формы (словарь полей формы и их значений)
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comment']}"
            send_mail(subject, message, 'ganichevkirill9@gmail.com',
                      [cd['to']])
            sent = True
    else:  # GET -> пользователь получил форму и должен ее заполнить -> она должна быть пустой
        form = EmailPostForm()
    return render(request,  # рендерит шаблон с передачей поста и экземпляра формы
                  'blog/post/share.html',
                  {'post': post,
                   'form': form,
                   'sent': sent})


@require_POST  # Обработка только POST запросов
def post_comment(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    comment = None  # Если комментарий не был успешно сохранен, он будет иметь значение None
    # Комментарий был отправлен
    form = CommentForm(data=request.POST)  # В этот экземпляр мы передаем данные с формы из comment_form.html
    if form.is_valid():
        # Создать объект класса Comment, не сохраняя его в БД
        comment = form.save(commit=False)  # благодаря этому до окончательного сохранения мы можем изменять объект
        comment.post = post  # пост комментария это пост, под которым оставлен коммент, логичная хуйня
        comment.save()  # сохраняем в БД
    return render(request,
                  'blog/post/comment.html',  # шаблон будет отображать все хуйни, переданные в context
                  {'post': post,  # передает в шаблон пост, форму комментария и сам комментарий
                   'form': form,
                   'comment': comment})


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'body', config='russian')
            search_query = SearchQuery(query, config='russian')
            results = Post.published.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)  # ранг это типо насколько соответсвует/похоже на запрос
            ).filter(search=search_query).order_by('-rank')  # сортируем по похожести, по рангу
    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})
