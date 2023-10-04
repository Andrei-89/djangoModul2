from django.db.models.signals import post_save
from django.dispatch import receiver # импортируем нужный декоратор
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.utils.html import strip_tags


from .models import Post, Mailing, PostCategory
from django.contrib.auth.models import User
 
 
# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
# при подписки на категорию новостей на почту приходит уведомление о подписке
# @receiver(post_save, sender=Mailing)
def mailing_sabscribe(sender, instance, created, **kwargs):
    send_mail(
        subject=f'«Здравствуй, {instance.subscribers.username} подравляю ты подписался на новости!»',  # имя клиента и дата записи будут в теме для удобства
        message=f'В могужем разделе - {instance.category.name}', # сообщение с кратким описанием проблемы
        from_email = 'bulanov-rvp@yandex.ru',
        recipient_list = [instance.subscribers.email], # здесь список получателей. Например, секретарь, сам врач и так далее
    )

#При добавлении новой станьи она рассылается на почту подписчикам
# @receiver(post_save, sender=PostCategory)
def mailing_postcategory(sender, instance, **kwargs):
    users = Mailing.objects.filter(category=instance.category).values_list('subscribers', flat=True)
    subscribers = User.objects.filter(id__in=users)
    for subscriber in subscribers:
        send_mail(
            subject=f'Здравствуй {subscriber}, для тебя появилась новая новость!»',  # имя клиента и дата записи будут в теме для удобства
            message=f'В могужем разделе - {instance.category.name}!, она называется: {instance.post.titel}\n Ссылка на статью: {instance.post.get_absolute_url()}',
            from_email = 'bulanov-rvp@yandex.ru',
            recipient_list = [subscriber.email],
        )

#При добавлении новой станьи она рассылается на почту подписчикам через шаблон
# @receiver(post_save, sender=PostCategory)
def send_mail_to_subscribers(post, sender, instance):
    subject = 'Новая статья'
    users = Mailing.objects.filter(category=instance.category).values_list('subscribers', flat=True)
    html_message = render_to_string('newsletter.html', {'post': post})
    plain_message = strip_tags(html_message)
    from_email = 'bulanov-rvp@yandex.ru'
    to_emails = [subscriber.email for subscriber in User.objects.filter(id__in=users)]

    # Получение URL-адреса статьи
    post_url = post.get_absolute_url()

    # Добавление ссылки на статью в содержимое письма
    html_message += f'<p>Ссылка на статью: <a href="{post_url}">{post.title}</a></p>'

    send_mail(subject, plain_message, from_email, to_emails, html_message=html_message)


#Раз в неделю подписчикам приходит список всех статей добавленных в течение недели 

# @receiver(post_save, sender=PostCategory)
def mailing_postcategory_week(sender, instance, **kwargs):
    posts = Post.objects.filter(postCategory=instance.category).values('id', 'titel', 'text')
    users = Mailing.objects.filter(category=instance.category).values_list('subscribers', flat=True)
    subscribers = User.objects.filter(id__in=users)
    
    for subscriber in subscribers:
        post_list = []
        for post in posts:
            post_list.append({
                'id': post['id'],
                'titel': post['titel'],
                'text': post['text'],
            })
        
        html_content = render_to_string(
            'subscribers/mailing_post_add.html',
            {
                'posts': post_list,
                'username': subscriber,
            }
        )
        
        msg = EmailMultiAlternatives(
            subject='Новые статьи в разделе {}'.format(instance.category.name),
            body='Здравствуй, {}. Новые статьи в твоём любимом разделе!'.format(subscriber.username),
            from_email='bulanov-rvp@yandex.ru',
            to=[subscriber.email],
        )
        
        msg.attach_alternative(html_content, "text/html")
        msg.send()

# receiver(post_save, sender=PostCategory)
def mailing_postcategory_week(sender, instance, post_id, **kwargs):
    post = Post.objects.get(id=post_id)
    users = Mailing.objects.filter(category=instance.category).values_list('subscribers', flat=True)
    subscribers = User.objects.filter(id__in=users)
    for subscriber in subscribers:
         # создание HTML-контента письма, которое будет отправлено клиенту
        html_content = render_to_string( 
            'subscribers/mailing_post_add.html',
            {
                'post': instance,
                'text': instance.post.text,
                'username': instance.category.name,
            } 
        )
        # В конструкторе класса EmailMultiAlternatives создается объект msg, в котором указываются тема письма, текст письма, отправитель и получатель
        msg = EmailMultiAlternatives(
            subject=f'{post.titel}',
            body=f'Здравствуй, {subscriber}. '
            'Новая статья в твоём любимом разделе!', #  это то же, что и message
            from_email='bulanov-rvp@yandex.ru',
            to=[subscriber.email], # это то же, что и recipients_list
        )
        # с помощью метода attach_alternative, добавляется HTML-контент письма.
        msg.attach_alternative(html_content, "text/html") # добавляем html
        msg.send() # отсылаем
