from django.urls import path  # Функция path используется для определения URL-путей
from . import views

app_name = 'blog'  # Это позволит различать URL-путей между разными приложениями в проекте.

urlpatterns = [  # URL-пути для вашего приложения. Каждый элемент списка представляет один путь.
    # представления поста
    # path('', views.post_list, name='post_list'),  # Не принимает аргументов и соотносится с представлением post_list
    path('', views.PostListView.as_view(), name='post_list'),  # as_view преобразует в представление.
    path('<int:year>/<int:month>/<int:day>/<slug:post>', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id/comment/', views.post_comment, name='post_comment')
]  # <parameter> - записывается в таких скобках
