# from celery import shared_task

# import django.contrib.auth
# from .models import Post, Mailing
# from django.template.loader import render_to_string
# from django.core.mail import EmailMultiAlternatives

# from datetime import datetime, timedelta

def send_mails():
	# print('Привет это задача с бекграунда!')
	pass
	

# def do_mailing():
#     end_date = datetime.now().replace(hour=8, minute=0, second=0)#задается дата окончания (`end_date`), которая устанавливается на сегодняшний день, но со временем 8:00:00
#     start_date = end_date - timedelta(weeks=1)#дата начала (`start_date`), которая устанавливается на неделю назад от `end_date`. 

#     for user in django.contrib.auth.get_user_model().objects.all():
#         send_post = Post.objects.filter(
#             creation_time__range=(start_date, end_date),
#             categories__in=Mailing.objects.filter(subscribers=user).
#             values('category')
#             )
#         if send_post:
#             html_content = render_to_string(
#                 'mailing_list.html',
#                 {
#                     'post': send_post,
#                     'user': person,
#                 }
#             )

#             posts_list_txt = ', '.join([post.header for post in send_post])
#             msg = EmailMultiAlternatives(
#                 subject='Список новых статей',
#                 body=f'Здравствуй, {person.username}.'
#                 f'Список новых статей за неделю:'
#                 f'{posts_list_txt}',
#                 from_email='sf.testmail@yandex.ru',
#                 to=[person.email],
#             )
#             msg.attach_alternative(html_content, "text/html")

#             msg.send()