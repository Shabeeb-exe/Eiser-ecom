from django import template

register = template.Library()

@register.filter
def remove_decimal_if_zero(value):
    """
    Removes the decimal point and trailing zeros if the decimal part is .00.
    Example: 1,19,690.00 -> 1,19,690
    """
    if isinstance(value, str):
        if '.' in value:
            integer_part, decimal_part = value.split('.')
            if decimal_part == '00':
                return integer_part
    return value