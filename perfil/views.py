from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.edit import FormView
from django.contrib import messages
from perfil.forms import (
SetPasswordFormCustom,
FuncionarioForm,
UnidadeForm,
CustomAuthenticationForm,
PasswordChangeFormCustom,
)
from .models import Funcionario, Unidade
from perfil.decorators import verificar_funcionario


@verificar_funcionario()
@login_required
def perfil(request):
    funcionario = Funcionario.objects.get(id=request.user.funcionario.id)
    context = {'funcionario': funcionario} 
    return render(request, 'perfil/perfil.html', context)


@verificar_funcionario()
@login_required
def atualizar_perfil(request, id):
    funcionario = get_object_or_404(Funcionario, pk=id)
    form = FuncionarioForm(request.POST,  request.FILES or None, instance=funcionario)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            redirect('perfil:perfil')
        else:
            messages.error(request, 'Erro campos inválidos.')
            print('erro: ', form.errors)

    return render(request, 'perfil/perfil.html', {'form': form, 'funcionario': funcionario})


@login_required
def set_password(request):
    funcionario = request.user.funcionario
    if request.method == 'POST':
        form =  PasswordChangeFormCustom(data=request.POST,  user=request.user)

        old_password = form.data["old_password"]
        admissao = str(form.data["admissao"])
        admissao_banco_dados = str(request.user.funcionario.admissao)

        if not request.user.check_password(old_password):
            messages.error(request, "O número de registro não é válido.")
            return render(request, "perfil/modificar_senha.html", {'form': form})

        elif admissao.replace('/', '') != admissao_banco_dados.replace('/', ''):
            messages.error(request, "A data de admissão está inválida")
            return render(request, "perfil/modificar_senha.html", {'form': form})
        
        elif len(form.data['new_password1']) < 8:
            messages.error(request, "A senha precisa ser maior que 8 dígitos ser composta por letras e números e uma letra maiúscula ")
            return render(request, "perfil/modificar_senha.html", {'form': form})

        elif str(form.data['new_password1']) != str(form.data['new_password2']):
            messages.error(request, "As senha não se combinam.")
            return render(request, "perfil/modificar_senha.html", {'form': form})
        
        if form.is_valid():
            form.save()
            funcionario.primeiro_acesso = False
            funcionario.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Senha alterada com sucesso!")
            return redirect('perfil:perfil')
        else:
            context = {'form': form}
            return render(request, "perfil/modificar_senha.html", context)
    else:
        form = PasswordChangeFormCustom(user=request.user)
        context = {'form': form}
        return render(request, "perfil/modificar_senha.html", context)


@login_required
def meu_logout(request):
    logout(request)
    return redirect('login')


# class ResetaSenha(FormView):
#     template_name = 'perfil/modificar_senha.html'
#     form_class = SetPasswordFormCustom
#     success_url = '/resetar_senha/'

#     def form_valid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
#         return super().form_valid(form)
    
#     def post(self, request, *args, **kwargs):
#         self.object = None
#         return super().post(request, *args, **kwargs)


def ResetaSenha(request):
    form = SetPasswordFormCustom(data=request.POST, user=None)
    unidade  = Unidade.objects.all()
    # re = Funcionario.objects.all().filter(unidade=unidade)

    if form.is_valid():
        form.save()
        return redirect('perfil:enviar')
    else:
        return render(request, 'perfil/reset_senha.html', {'form': form, 'unidade': unidade}) 
        
    

class Login(auth_views.LoginView):
    authentication_form = CustomAuthenticationForm
    template_name= 'perfil/login.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unidade  = Unidade.objects.all()
        re = Funcionario.objects.filter(unidade=unidade)
        context.update({'unidade': unidade,
                        're': re,
                      })
        return context
