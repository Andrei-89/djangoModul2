from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views import View
from django_filters import FilterSet
from django.utils import timezone
from django.urls import reverse
from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import RegisterForm
from .filters import PostFilter 
from django.shortcuts import redirect 
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *



class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'sign/user.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context
    
@login_required
def upgrade_me(request):
   user = request.user
   author_group = Group.objects.get(name='authors')
   if not request.user.groups.filter(name='authors').exists():
       author_group.user_set.add(user)
   return redirect('news:user')


class RegisterView(CreateView):
   model = User
   form_class = RegisterForm
   template_name = 'sign/signup.html'
   success_url = '/news/search/'

   def form_valid(self, form):
        user = form.save()
        group = Group.objects.get_or_create(name='common')[0]
        user.groups.add(group) # добавляем нового пользователя в эту группу
        user.save()
        return super().form_valid(form)

class LoginView(FormView):
   model = User
   form_class = LoginForm
   template_name = 'sign/login.html'
   success_url = '/user/'
  
   def form_valid(self, form):
       username = form.cleaned_data.get('username')
       password = form.cleaned_data.get('password')
       user = authenticate(self.request,username=username, password=password)
       if user is not None:
           login(self.request, user)
       return super().form_valid(form)
  
  
class LogoutView(LoginRequiredMixin, TemplateView):
   template_name = 'sign/logout.html'
  
   def get(self, request, *args, **kwargs):
       logout(request)
       return super().get(request, *args, **kwargs)


# @method_decorator(login_required, name='dispatch') 
class PostList(ListView):
    model = Post
    template_name = 'news/news_filter.html' 
    context_object_name = 'posts' 
    queryset = Post.objects.all().order_by('-dataCreation')
    paginate_by = 3

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['time_now'] = timezone.localtime(timezone.now()) # добавим переменную текущей даты time_now
       context['value1'] = Post.objects.filter(categoryType = 'NW') # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого фильтра
       context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
       context['choices'] = Post.CATEGORY_CHOICES
       context['form'] = PostForm()
    #    context['choices_category'] = Category.objects.all()
       return context
    
    def post(self, request, *args, **kwargs):
       form = self.form_class(request.POST) 
       if form.is_valid():
           form.save()
       return super().get(request, *args, **kwargs)
    
    # def addpage(request):
    #     form_test = PostTestForm()
    #     return render(request, 'news/news_filter.html', {'form_test':form_test})
    
    

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

# дженерик для создания объекта. Надо указать только имя шаблона и класс формы, который мы написали в прошлом юните. Остальное он сделает за вас
class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'news/post_create.html'
    form_class = PostForm
    permission_required = ('news.add_post', 'news.change_post')
    
# дженерик для редактирования объекта

class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'news/post_create.html'
    form_class = PostForm
    permission_required = ('news.add_post', 'news.change_post')
    success_url = reverse_lazy('news:posts')


    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

# дженерик для удаления товара
# @method_decorator(login_required, name='dispatch')
class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    # переход на страницу поиска новостей
    success_url = reverse_lazy('news:posts') # не забываем импортировать функцию reverse_lazy из пакета django.urls


class PostCard(DetailView):
    model = Post
    template_name = 'news/post_card.html' 

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