from django import template
from myprofile.models import FavoriteProduct

register = template.Library()

@register.simple_tag(takes_context=True)
def is_favorite(context, product):
    request = context['request']
    if not request.user.is_authenticated:
        return False
    
    return FavoriteProduct.objects.filter(
        user=request.user, 
        product=product
    ).exists()