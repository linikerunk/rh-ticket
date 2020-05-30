from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User 
from django.contrib import messages
from perfil.forms import FuncionarioForm, PerfilForm, UnidadeForm
from .models import Funcionario, Perfil, Unidade


# Create your views here.

@login_required
def perfil(request):
    perfil = Perfil.objects.get(id=request.user.id)
    funcionario = perfil.funcionario
    context = {'perfil': perfil, 'funcionario': funcionario} 
    return render(request, 'perfil/perfil.html', context)

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

    return render(request, 'perfil/perfil.html', {'form': form, 'funcionario': funcionario})

def login(request):
    context = {}
    return render(request, 'perfil/login.html', context)

@login_required
def meu_logout(request):
    logout(request)
    return redirect('login')