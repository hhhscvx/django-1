from django.urls import path  # Функция path используется для определения URL-путей
from . import views

app_name = 'blog'  # Это позволит различать URL-путей между разными приложениями в проекте.

urlpatterns = [  # URL-пути для вашего приложения. Каждый элемент списка представляет один путь.
    # представления поста
    path('', views.post_list, name='post_list'),  # Не принимает аргументов и соотносится с представлением post_list
    path('<int:id>/', views.post_detail, name='post_detail'),  # принимает аргумент id и соотносится в view post_detail
]  # <parameter> - записывается в таких скобках
