from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Praxis


# checkt ob eine user eingeloggt ist, falls nicht wird er umgeleitet.

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('arzt-home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


# entwurf um mehreren userrollen zugriff zu gewähren

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')

        return wrapper_func

    return decorator


# checkt ob eine user der arztgruppe gehört, falls nicht wird er umgeleitet.

def arzt_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        try:
            if request.user.is_superuser:
                return redirect('/admin-page')
            else:
                if request.user.groups.exists():
                    group = request.user.groups.all()[0].name

                if group == 'arzt':
                    return view_func(request, *args, **kwargs)

                if group == 'apotheke':
                    return redirect('apotheke-home')
        except AttributeError:
            return redirect('praxis-home')

    return wrapper_function

def praxis_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        try:
            if request.user.is_superuser:
                return redirect('/admin-page')
            else:
                return redirect('arzt-home')
        except AttributeError:
            return view_func(request, *args, **kwargs)

    return wrapper_function


# checkt ob eine user der apothekengruppe gehört, falls nicht wird er umgeleitet.

def apotheke_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        try:
            if request.user.is_superuser:
                return redirect('/admin-page')
            else:
                if request.user.groups.exists():
                    group = request.user.groups.all()[0].name

                if group == 'arzt':
                    return redirect('arzt-home')

                if group == 'apotheke':
                    return view_func(request, *args, **kwargs)
        except AttribueError:
            return redirect('praxis-home')

    return wrapper_function


