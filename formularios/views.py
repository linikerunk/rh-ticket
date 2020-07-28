# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User # Chamados
from django.core.paginator import Paginator
from django.contrib import messages

from chamados.models import Ticket, Categoria, SubCategoria
from perfil.models import Funcionario, Unidade
from perfil.forms import FuncionarioForm
from .forms import JustificativaAusenciaForm 
from .models import JustificativaAusencia

from perfil.decorators import *


@verificar_funcionario()
@login_required
def enviar_justificativa_ausencia(request):
    if request.method == 'POST':
        form = JustificativaAusenciaForm(request.POST or None)

        if form.is_valid():
            justificativa_ausencia = form.save(commit=False)
            justificativa_ausencia.funcionario = request.user.funcionario
            justificativa_ausencia.save()
            messages.success(request, 'Ticket de "Justificativa de Ausência" enviado com sucesso!')
            return redirect('chamados:enviar')
        else:
            messages.error(request, f"\tErro ao enviar : data inicio ou data fim está diferente do especificado.")
            return render(request, 'formularios/justificativa_ausencia.html', {'form': form})
    else:    
        return render(request, 'formularios/justificativa_ausencia.html', {})
        

def enviar_agendamento_ferias(request):
    pass
