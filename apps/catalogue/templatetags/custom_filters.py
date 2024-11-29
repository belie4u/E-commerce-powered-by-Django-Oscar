from django import template
from apps.partner.models import StockRecord

register = template.Library()

@register.filter(name = 'get_range')
def get_range(value, arg=None):
    return range(int(value)) if arg is None else range(int(value), int(arg))


@register.simple_tag
def get_stock_record(product):

    stock_record = StockRecord.objects.filter(product=product).first()
    if stock_record:
        return{
            "partner":stock_record.partner.name,
            "sku":stock_record.partner_sku
        }
    return None
