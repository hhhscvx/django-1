from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']  # элементы сортировки
    list_filter = ['status', 'created', 'publish', 'author']  # справа filter
    search_fields = ['title', 'body']  # значения, по которым можно осуществлять поиск
    prepopulated_fields = {'slug': ('title',)}  # при создании поста slug автоматически заполняется как title
    raw_id_fields = ['author']  # при создании поста добавляется поиск авторов для упрощения жизни
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']  # сортировка по умолчанию
