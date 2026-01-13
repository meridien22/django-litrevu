from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    """Allows you to specify the author of the post by using their first name or a personal pronoun.

    Args:
        context : Context in which the function is called.
        user : User logged in at the time the function was called.

    Returns:
        string: The appropriate formula to refer to the author of the post.
    """
    if user == context['user']:
        return "Vous avez"
    return f"{user.username} a"
