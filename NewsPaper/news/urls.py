from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

app_name = 'news'

urlpatterns = [
    path('news/search/', PostList.as_view(), name='posts'),
    path('', cache_page(60)(CensoredList.as_view())),
    path('news/<int:pk>/', PostDetail.as_view(), name='post'),    
    path('news/', CensoredList.as_view()),
    path('news/add/', PostCreateView.as_view(), name='post_create'), 
    path('news/<int:pk>/edit', PostUpdateView.as_view(), name='post_update'),
    path('news/<int:pk>/card', PostCard.as_view(), name='post_card'),
    path('news/<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'), 
    path('user/', IndexView.as_view(), name='user'),
    path('upgra te/', upgrade_me, name='upgrate'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('subscribers/', SubscribersView.as_view(), name='subscribers'),
    


    # path('filter/all/', PostAllView.as_view()),
    # path('news/demo/', News.as_view()),
    # path('news1/', post),
    # path('news', views.index),
]
#     path('about', views.about),

# создали функцию индекс котораяотображает сообщение 