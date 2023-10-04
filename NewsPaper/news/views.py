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
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.core.cache import cache


from .models import *
from .forms import *

# Отправляем форму о том что он успешно подписался на категорию
class SubscribersView(CreateView):
    model = Mailing
    template_name = 'subscribers/make_subscribers.html'
    form_class = SubscribersForm
    success_url = '/news/'

    # def get(self, request, *args, **kwargs):
    #     form = self.form_class()
    #     print(form)

    def subscribe_add(self, request):
        categorys = request.POST.getlist('name')
        user = self.user.username
        for category in categorys:
            subscriber = Mailing(categorys=category, subscriber=user)
            subscriber.save()


# class SubscribersForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         self.authorized_user = kwargs.pop('authorized_user', None)
#         super(SubscribersForm, self).__init__(*args, **kwargs)
        
#         if self.authorized_user:
#             self.fields['subscribers'].initial = self.authorized_user
    
#     class Meta:
#         model = Mailing
#         fields = ['category', 'subscribers']
#         widgets = {
#             'category': forms.Select(attrs={'class': 'form-select'}),
#         }


    # def form_valid(self, form):
    #     subscribe = form.save()
    #     print (subscribe)
        # user = Group.objects.get_or_create(name='common')[0]
        # subscribe.groups.add(user) # добавляем нового пользователя в эту группу
        # subscribe.save()
        # return super().form_valid(form)



    # def get(self, request, *args, **kwargs):
    #     form = self.form_class()
    #     return render(request, self.template_name, {'form': form})

    #В этом коде мы создаем экземпляр формы SubscribersForm с данными из запроса request.POST. Затем мы проверяем, является ли форма валидной. Если форма валидна, мы сохраняем экземпляр модели Subscriber, устанавливаем поле userThrough равным экземпляру пользователя request.user и сохраняем модель.
   
    # def post(self, request, *args, **kwargs):
    #     category_names = request.POST.getlist('category')
    #     for category in category_names:
    #         form = CategorySubscriber(category=category, user=request.user,)
    #         if form.is_valid():
    #             form.save()
    #     return redirect('news:user')

        #Если форма не валидна, мы возвращаем шаблон с формой и ошибками.
        # return render(request, self.template_name, {'form': form})
        

        # form = Subscriber(
	    # userThrough=request.user.username,
        # categoryThrough=request.POST['categoryThrough'],
        # )
        # if form.is_valid():
        #     form.save()
        # return redirect('news:user')
    
     # def get(request):
    #     if request.method == 'POST':
    #         form = SubscribersForm(request.POST)
    #         if form.is_valid():
    #             subscriber = form.save(commit=False)
    #             subscriber.user = request.user
    #             subscriber.save()

    #             # Проверяем наличие email у пользователя
    #             if request.user.email:
    #                 # Отправляем сообщение на email пользователя
    #                 # Ваш код отправки сообщения

    #                 return redirect('news:user')  # Перенаправляем на страницу успешной подписки
    #     else:
    #         form = SubscribersForm()

    #     return render(request, 'subscribe.html', {'form': form})

    # def send_newsletter(category):
    #     subscribers = category.subscribers.filter(id=user.id).exists()
    #     for subscriber in subscribers:
    #         subject = f'{category.subscribers} - Вы подписаны на новостную категорию {category.name}',
    #         message = 'Поздравляю!',
    #         from_email = 'bulanov-rvp@yandex.ru',
    #         # заменить на почту пользователя
    #         recipient_list = ['bylich07@mail.ru'],
    #         html_message = render_to_string('newsletter.html', {'category': category, 'subscriber': subscriber}),
    #         send_mail(subject, message, from_email, recipient_list, html_message=html_message),
    #     return redirect('news:user')




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

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset) 
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj
    
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['time_now'] = timezone.localtime(timezone.now())
       return context

    
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
    success_url = reverse_lazy('news:posts')
    # При выходе новости отправляем новость тем читателям,которые подписались (как функцию при добавлении статьи)
    
    # def send_newsletter(category):
    #     subscribers = category.subscribers.filter(кто подписался)
    #     for subscriber in subscribers:
    #         subject = category.name
    #         message = render_to_string('newsletter.html', {'category': category, 'subscriber': subscriber})
    #         send_mail(subject, '', 'noreply@example.com', [subscriber.email], html_message=message)
    
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