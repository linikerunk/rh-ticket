from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name='nome_capitalize')
def nome_capitalize(value):
    string = value.split(" ")
    string = (string[0].capitalize() + " " + string[-1].capitalize())
    return string


@register.filter(name='belong_group')
def belong_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


@register.filter(name='group_name')
def group_name(user):
    # group = Group.objects.get(name=)
    pass