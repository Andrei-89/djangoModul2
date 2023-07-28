from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import *
from django.utils import timezone
 
 
class PostList(ListView):
    model = Post
    template_name = 'news/news_all.html' 
    context_object_name = 'posts' 
    queryset = Post.objects.all().order_by('-dataCreation')

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['time_now'] = timezone.localtime(timezone.now()) # добавим переменную текущей даты time_now
       context['value1'] = Post.objects.filter(categoryType = 'NW') # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого фильтра
       return context
    

class PostDetail(DetailView):
    model = Post
    template_name = 'news/news_one.html' 
    context_object_name = 'post' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.__str__()
        return context
    
class CensoredList(ListView):
    model = Post
    template_name = 'news/news_read.html' 
    context_object_name = 'posts' 
    queryset = Post.objects.all().order_by('-dataCreation')

        
    # def index(request):
    #     return HttpResponse(f'<h2> Hellou word \n Привет!</h2>')

    
    # def get_posts_count(self):
    #     count = Post.objects.all()
    #     return HttpResponse(f'{count}')
    
    # def post_list(request):
    #     posts = Post.objects.filter(categoryType='AR')
    #     context = {'posts': posts}
    #     return render(request, 'post_list.html', context)



 # написали как должен реагировать по запросу например path('', views.index),

# def about(request):
#         return HttpResponse('<h2>Это мы и он нас!</h2>')

# def product(request, product_id):
#         out = 'Product #{0}'.format(product_id)
#         return HttpResponse(out)