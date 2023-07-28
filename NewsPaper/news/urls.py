from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('table/', PostList.as_view()),
    path('news/<int:pk>/', PostDetail.as_view()),
    path('news/', CensoredList.as_view())
    # path('news1/', post),

    # path('news', views.index),
]
#     path('about', views.about),

# создали функцию индекс котораяотображает сообщение 