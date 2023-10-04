from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from .models import *
from django import forms


class BasicSignupForm(SignupForm):
  
   def save(self, request):
       user = super(BasicSignupForm, self).save(request)
       basic_group = Group.objects.get_or_create(name='common')[0]
       basic_group.user_set.add(user)
       return user


class LoginForm(AuthenticationForm):
    class Meta:
       model = User
       fields = (
         "username",
         "password",
           )
       

class RegisterForm(UserCreationForm):
   password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Password')
   password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Confirm Password')
  
   class Meta:
       model = User
       fields = (
         "username",
         "email",
         "password1",
         "password2",
           )
       widgets = {
           'username': forms.TextInput(attrs={'class': 'form-control'}),
           'email': forms.EmailInput(attrs={'class': 'form-control'}),
       }
      
   def clean(self):
       username = self.cleaned_data.get('username')
       email = self.cleaned_data.get('email')
       if User.objects.filter(username=username).exists():
           raise forms.ValidationError("Пользователь с таким именем уже существует")
       if User.objects.filter(email=email).exists():
           raise forms.ValidationError("Пользователь с таким email уже существует")
       return super().clean()
   
       
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

class SubscribersForm(ModelForm):
    class Meta:
       model = Mailing
       fields = ['category', 'subscribers']
      
       widgets = {
         'category' : forms.Select(attrs={
           'class': 'form-select',
         }),
       }
    def __init__(self, *args, **kwargs):
        super(SubscribersForm, self).__init__(*args, **kwargs)
        self.fields['category'].label_from_instance = lambda obj: obj.name
        
# class SubscribersForm(forms.ModelForm):
#     class Meta:
#         model = Mailing
#         fields = '__all__'
#         widgets = {
#             'category': forms.CheckboxSelectMultiple
#         }
#     def __init__(self, *args, **kwargs):
#         super(SubscribersForm, self).__init__(*args, **kwargs)
#         self.fields['category'].label_from_instance = lambda obj: obj.name
        
  
    

# class PostTestForm(forms.Form):
#     # author = forms.ModelChoiceField(queryset=Author.objects.all())
#     categoryType = forms.Select()
#     postCategory = forms.Select()
#     titel = forms.TextInput()
#     text = forms.Textarea()
#     post = Post(categoryType=categoryType, postCategory=postCategory, titel=titel, text=text)
#     post.save()