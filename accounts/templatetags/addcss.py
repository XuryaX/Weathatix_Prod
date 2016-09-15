'''
Created on 26-Jun-2016

@author: shaur
'''
from django import template
register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={"class":css})