from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False,  # значит что заполнять необязательно
                              widget=forms.Textarea)  # like <input type='textarea'>


class CommentForm(forms.ModelForm):
    class Meta:  # Связывает форму с моделью
        model = Comment  # поля формы будут отображать поля Модели Comment
        fields = ['name', 'body']  # поля формы, которые будут отображаться


class SearchForm(forms.Form):
    query = forms.CharField()
