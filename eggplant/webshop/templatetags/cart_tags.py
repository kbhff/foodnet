from django import template
from django.core.urlresolvers import reverse_lazy
from django.template.base import TemplateSyntaxError

register = template.Library()


@register.simple_tag
def cart_action(action, product_id, quantity):
    if action == 'remove':
        url = reverse_lazy('webshop:remove_from_cart')
    if action == 'add':
        url = reverse_lazy('webshop:add_to_cart')
    else:
        raise TemplateSyntaxError("action not supported")
    fmt = {
        'action': url,
        'product_id': int(product_id),
        'quantity': int(quantity),
    }
    html = '''
    <form action="{action}">
        <input name="product_id" values="{product_id}"/>
    </form>'''.format(fmt)
    return html
