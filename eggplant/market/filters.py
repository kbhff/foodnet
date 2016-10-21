import django_filters
from django.db.models.fields import BLANK_CHOICE_DASH
from django.forms.widgets import flatatt
from django.utils.encoding import force_text
from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from .models.inventory import Product, ProductCategory


class LinksGroupWidget(django_filters.widgets.LinkWidget):

    def render(self, name, value, attrs=None, choices=()):
        if not hasattr(self, 'data'):
            self.data = {}
        if value is None:
            value = ''
        base_attrs = {
        }
        base_attrs.update(attrs)
        final_attrs = self.build_attrs(base_attrs)
        output = ['<p%s>' % flatatt(final_attrs)]
        options = self.render_options(choices, [value], name)
        if options:
            output.append(options)
        output.append('</p>')
        return mark_safe('\n'.join(output))

    def render_option(self, name, selected_choices,
                      option_value, option_label):
        option_value = force_text(option_value)
        if option_label == BLANK_CHOICE_DASH[0][1]:
            option_label = _("All")
        data = self.data.copy()
        data[name] = option_value
        selected = data == self.data or option_value in selected_choices
        try:
            url = data.urlencode()
        except AttributeError:
            url = urlencode(data)
        if selected:
            attrstr = ' class="btn btn-success"'
        else:
            attrstr = ' class="btn btn-default"'
        return self.option_string() % {
            'attrs': attrstr,
            'query_string': url,
            'label': force_text(option_label)
        }

    def option_string(self):
        return '<a%(attrs)s href="?%(query_string)s">%(label)s</a>'


class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(
        label='',
        help_text='',
        queryset=ProductCategory.objects.filter(),
        widget=LinksGroupWidget()
    )

    class Meta:
        model = Product
        fields = [
            'category',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        extra = {
            'empty_label': 'All available products',
        }
        self.filters['category'].extra.update(extra)
