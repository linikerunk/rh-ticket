from functools import wraps

from django.shortcuts import redirect


def verificar_funcionario(redirect_to='perfil:set_password'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.id == None:
                pass
            elif request.user.funcionario.primeiro_acesso is True:
                return redirect(redirect_to)
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator 