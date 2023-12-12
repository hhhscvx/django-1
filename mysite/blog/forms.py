from django import forms


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False,  # значит что заполнять необязательно
                              widget=forms.Textarea)  # like <input type='textarea'>
