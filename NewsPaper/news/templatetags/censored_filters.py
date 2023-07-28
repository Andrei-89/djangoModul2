from django import template
from django.utils.safestring import mark_safe
# import news.src.banned_words  as words

banned_words = ['Власт', 'негодя', 'НКВД', 'кладбищ', 'правлени']
 
register = template.Library()

@register.filter(name='censor') 
def censor(value):
    for word in banned_words:
        letter = ''
        for i in range(len(word)):
            letter += '*'
        value = value.replace(word, letter)
    return mark_safe(value)

