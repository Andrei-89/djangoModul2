from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache
from django import forms

class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя") # опционально, можно не указывать
    last_name = forms.CharField(label = "Фамилия") # опционально

    class Meta:
        model = User
        fields = ("username", 
                  "first_name", # опционально
                  "last_name", # опционально
                  "email", 
                  "password1", 
                  "password2", )
        
class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

class Author(models.Model):
    autorUser = models.OneToOneField(User, on_delete=models.CASCADE) #для связи автора с юзером
    ratingAuthor = models.SmallIntegerField(default=0)

    def apdate_rating(self):
        postRat = self.post_set.all().aggregate(postRating=Sum('rating'))
        pRat = 0

        if postRat.get('postRating') is not None:
            pRat += postRat.get('postRating')

        commentRat = self.autorUser.comment_set.all().aggregate(commentRating=Sum('rating'))
        cRat = 0

        if commentRat.get('commentRating') is not None:
            cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()




class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    ARTICLE = 'AR'
    NEWS = 'NW'
    CATEGORY_CHOICES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]
    categoryType = models.CharField(max_length = 2,  choices = CATEGORY_CHOICES, default=ARTICLE)
    dataCreation = models.DateTimeField(auto_now_add = True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    titel = models.CharField(max_length = 128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0) 

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'
    
    def get_absolute_url(self):
        return reverse('news:post', args=[str(self.pk)])
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}') # затем удаляем его из кэша, чтобы сбросить его

    
    
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    

class Mailing(models.Model):
    subscribers = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dataCreation = models.DateTimeField(auto_now_add = True)
    rating = models.SmallIntegerField(default=0) 

    def __str__(self):
        try:
            return self.commentPost.author.autorUser.username
        except:
            return self.commentUser.username

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
