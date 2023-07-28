from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    autorUser = models.OneToOneField(User, on_delete=models.CASCADE) #для связи автора с юзером
    ratingAuthor = models.SmallIntegerField(default=0)

    def apdate_rating(self):
        postRat = self.post_set.all().aggregate(postRating=Sum('rating')) #Получаем все наши посты автора агригатором работаем с множеством записей и суммируем все поля значений rating
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.all().aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


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
    

class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


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
