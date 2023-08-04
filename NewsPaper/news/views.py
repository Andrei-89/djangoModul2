from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views import View
from django_filters import FilterSet
from .models import *
from django.utils import timezone
from django.core.paginator import Paginator
from django.shortcuts import render
from .filters import PostFilter 
 
 
class PostList(ListView):
    model = Post
    template_name = 'news/news_filter.html' 
    context_object_name = 'posts' 
    queryset = Post.objects.all().order_by('-dataCreation')
    paginate_by = 10

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['time_now'] = timezone.localtime(timezone.now()) # добавим переменную текущей даты time_now
       context['value1'] = Post.objects.filter(categoryType = 'NW') # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого фильтра
       context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
      
       return context
    

class PostAllView(ListView):
    model = Post
    template_name = 'news/news_all.html' 
    context_object_name = 'posts' 
    queryset = Post.objects.all().order_by('-dataCreation')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = timezone.localtime(timezone.now()) # добавим переменную текущей даты time_now
        context['value1'] = Post.objects.filter(categoryType = 'NW') # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого фильтра
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())

        return context

    
class PostDetail(DetailView):
    model = Post
    template_name = 'news/news_one.html' 
    context_object_name = 'post' 
    
class CensoredList(ListView):
    model = Post
    template_name = 'news/news_read.html' 
    context_object_name = 'posts'
    queryset = Post.objects.all().order_by('-dataCreation')

class News(View):
   def get(self, request):
       posts = Post.objects.all().order_by('-dataCreation')
       p = Paginator(posts, 2)
       posts = p.get_page(request.GET.get('page', 2))
       data = {
       'posts': posts,
       }

       return render(request, 'news/news_filter.html', data)

class PostFilter(FilterSet):
    class Meta:
       model = Post
       template_name = 'news/news_filter.html' 
       fields = {
           'dataCreation': ['gt'],
           'categoryType': ['exact'],
           'author': ['exact'],
           'titel': ['icontains'],
        }

#

        
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