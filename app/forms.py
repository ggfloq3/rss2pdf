from django import forms

from app.models import ArticleCategory


class MyForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(queryset=ArticleCategory.objects.all())
    email = forms.EmailField()
    date1 = forms.DateTimeField()
    date2 = forms.DateTimeField()
