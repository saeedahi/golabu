from django import template
import jdatetime

register = template.Library()

@register.filter
def to_persian_digits(number):
    en = '0123456789'
    fa = '۰۱۲۳۴۵۶۷۸۹'
    return str(number).translate(str.maketrans(en, fa))

@register.filter
def to_shamsi(date):
    date = jdatetime.datetime.fromgregorian(datetime=date).strftime('%Y-%m-%d')
    return date