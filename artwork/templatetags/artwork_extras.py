from django import template

register = template.Library()


@register.filter
def isk(value):
    """
    Format number as Icelandic currency style.

    Example:
    180000 -> 180.000
    """

    if value is None:
        return ""

    value = int(value)

    return f"{value:,}".replace(",", ".")