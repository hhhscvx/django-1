from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'  # Можно обращаться как Post.Status.choices(both)(like items)/labels(1)/values(DF, PB)
        PUBLISHED = 'PB', 'Published'  # короче эта хуйня это буквально словарь (словарь = key, value)

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')  # Сверяет уникальность по Дате
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')

    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']  # сортирован по паблишу (время публикации поста), но в обратном порядке (-)
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

    tags = TaggableManager()


class Comment(models.Model):
    post = models.ForeignKey(Post,  # коммент зависит от поста, удалят Пост - удалятся нахуй все комменты
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=35)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
