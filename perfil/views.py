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
    form = FuncionarioForm(request.POST, instance=funcionario)
    if form.is_valid():
        form.save()
        messages.success(request, 'Perfil foi alterado com sucesso!')
    context = {'perfil': perfil, 'funcionario': funcionario, 'form': form} 
    return render(request, 'perfil/perfil.html', context)
