from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from .models import Profile
from tickets.models import Ticket

def developer_required(function):
    """
    Decorator to ensure the user has the 'Developer' role.
    """
    def wrap(request, *args, **kwargs):
        if request.user.profile.role == Profile.Role.DEVELOPER:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

def user_is_assigned_developer(function):
    """
    Decorator to ensure the user is the developer assigned to the ticket.
    """
    def wrap(request, pk, *args, **kwargs):
        ticket = Ticket.objects.get(pk=pk)
        if ticket.assigned_to == request.user:
            return function(request, pk, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

# An alternative way using Django's built-in decorator
def developer_required_django_version(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_authenticated and u.profile.role == Profile.Role.DEVELOPER,
        login_url='/accounts/login/',
        redirect_field_name=None
    )
    return decorated_view_func(view_func)