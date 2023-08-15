from django.urls import path
from . import views
from .views import *

app_name = 'news'

urlpatterns = [
    path('news/search/', PostList.as_view(), name='posts'),
    path('news/<int:pk>/', PostDetail.as_view()),
    path('news/', CensoredList.as_view()),
    path('news/add/', PostCreateView.as_view(), name='post_create'), 
    path('news/<int:pk>/edit', PostUpdateView.as_view(), name='post_update'),
    path('news/<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'), 

    # path('filter/all/', PostAllView.as_view()),
    # path('news/demo/', News.as_view()),
    # path('news1/', post),
    # path('news', views.index),
]
#     path('about', views.about),

# создали функцию индекс котораяотображает сообщение 