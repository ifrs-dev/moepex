from django import template

from events.models import Registration

register = template.Library()

@register.filter
def check(group, user):
    workload = {1: [1, 11, 12], 2: [2, 13, 14], 11:[1, 11], 12: [1, 12], 13: [2, 13], 14: [2, 14]}
    conflicts = workload[group.shift]
    return Registration.objects.filter(group__event__workload__in=conflicts, user=user).exists()

