from django.forms import ModelForm
from .models import *
from django import forms

class PostForm(ModelForm):
    class Meta:
       model = Post
    #    category = forms.ModelChoiceField(queryset=Category.objects.all())
    #    post = Category(name=category)
    #    post.save()
       fields = ['titel', 'categoryType', 'postCategory', 'author', 'text']
       widgets = {
         'titel' : forms.TextInput(attrs={
           'class': 'form-control',
           'placeholder': 'Создайте заголовок'
         }),
         'categoryType' : forms.Select(attrs={
           'class': 'form-select',
         }),
         'postCategory' : forms.SelectMultiple(attrs={
           'class': 'form-select',
         }),
         'author' : forms.Select(attrs={
           'class': 'form-select',
         }), 
         'text' : forms.Textarea(attrs={
           'class': 'form-control',
           'placeholder': 'Текст статьи'
         }),
       }

# class PostTestForm(forms.Form):
#     # author = forms.ModelChoiceField(queryset=Author.objects.all())
#     categoryType = forms.Select()
#     postCategory = forms.Select()
#     titel = forms.TextInput()
#     text = forms.Textarea()
#     post = Post(categoryType=categoryType, postCategory=postCategory, titel=titel, text=text)
#     post.save()