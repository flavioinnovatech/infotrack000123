# -*- coding: utf-8 -*-

try:
    from functools import wraps
except:
    from django.utils.functional import wraps

from itrack.system.models import System
from itrack.system.tools import findChild, isChild
from django.http import HttpResponseForbidden

def system_has_access():
    def decorator(func):
        def inner_decorator(request,*args, **kwargs):
            system = args[0]
            childs = findChild(request.session["system"])
            if isChild(int(system),childs):
                return func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden(u"Você não tem permissão para alterar esse sistema.")        
        return wraps(func)(inner_decorator)
    
    return decorator

