from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm 
from django.contrib import messages
from perfil.forms import FuncionarioForm, UnidadeForm
from .models import Funcionario, Unidade
from perfil.decorators import verificar_funcionario


@verificar_funcionario()
@login_required
def perfil(request):
    funcionario = Funcionario.objects.get(id=request.user.funcionario.id)
    print(funcionario)
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
            redirect('perfil')
        else:
            messages.error(request, 'Erro campos inválidos.')

    return render(request, 'perfil/perfil.html', {'form': form, 'funcionario': funcionario})


@login_required
def set_password(request):
    funcionario = request.user.funcionario
    if request.method == 'POST':
        form =  PasswordChangeForm(data=request.POST,  user=request.user)
        print("forms : ", form.fields)
        
        if form.is_valid():
            form.save()
            funcionario.primeiro_acesso = False
            funcionario.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Senha alterada com sucesso!")
            return redirect('perfil:perfil')
        else:
            context = {'form': form}
            return render(request, "perfil\modificar_senha.html", context)
    else:
        form = PasswordChangeForm(user=request.user)
        context = {'form': form}
        return render(request, "perfil\modificar_senha.html", context)


def login(request):
    context = {}
    return render(request, 'perfil/login.html', context)


@login_required
def meu_logout(request):
    logout(request)
    return redirect('login')