# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User # Chamados
from django.core.mail import send_mail, send_mass_mail
from django.core import serializers
from django.core.paginator import Paginator
from django.contrib import messages

from .models import Ticket, Categoria, SubCategoria
from perfil.models import Funcionario, Unidade
from .forms import TicketForm, TicketUpdateForm
from perfil.forms import FuncionarioForm
from perfil.decorators import *


# AJAX

def funcionario_login_ajax(request, id):
    re = request.GET.get('funcionario-login')
    response = {'re': re}
    return JsonResponse(response)


def funcionario_ajax(request, id):
    re_func = request.GET.get('re_func')
    funcionario  = Funcionario.objects.filter(re_funcionario=re_func).first()
    response = {}
    if funcionario:
        response = {"nome": funcionario.nome, 'email': funcionario.email}
    return JsonResponse(response)
        

def carregar_subcategorias(request, id):
    subcategoria = SubCategoria.objects.filter(categoria=id)
    print(subcategoria)
    data = serializers.serialize("json", subcategoria, fields=('id','nome'))
    response = {'data': data}
    return JsonResponse(response, safe=False)


# Sistema
@verificar_funcionario()
@login_required
def enviar(request):
    categoria = Categoria.objects.all()
    # ------------------------------------------------------------------------ #
    unidade = request.user.funcionario.unidade
    funcionario = request.user.funcionario
    if request.method == 'POST':
        form = TicketForm(request.POST,  request.FILES or None)
        email = request.POST.get('email')
        categoria_field = request.POST.get('categoria')
        subcategoria = request.POST.get('subcategoria')
        subcategoria = SubCategoria.objects.get(pk=subcategoria)
        form.instance.funcionario = funcionario
        form.instance.unidade = unidade
        texto = request.POST.get('texto')

        if form.is_valid():
            form.save()
            save_it = form.save()
            save_it.save()
            subject = "Novo chamado aberto"
            message = f"\tCategoria : {categoria_field}\n\tSubcategoria : {subcategoria}\n\t\
RE : {funcionario.re_funcionario}\n\tNome : {funcionario.nome}\n\tDescrição : {texto}\n\
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
            if str(unidade) == 'Salto':
                from_email = settings.EMAIL_HOST_USER
                recipient_list = ['pedro.melo@continental.com', 
                'andreia.nogueira@continental.com', 'fabiana.carvalho@continental.com']
            elif str(unidade) == 'Camaçari':
                from_email = 'rh.camacari@conti.com.br'
                recipient_list = ['Cristhiane.nascimento@continental.com', 'Elissandra.magalhaes@continental.com',
'Eloah.jesus@continental.com', 'evelyn.aguiar@continental.com', 'fabio.pinho@continental.com', 'Ila.cerqueira@continental.com', 
'Jorrelrison.tanan@continental.com', 'Leila.tavares@continental.com', 'Lelia.lima@continental.com', 'olivia.figueiredo@conti.com',
'rayssa.santos@continental.com', 'Tatiane.custodio@continental.com', 'thaissa.juliao@conti.com']
            elif str(unidade) == 'Ponta Grossa':
                from_email = settings.EMAIL_HOST_USER
                recipient_list = ['']
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)
            messages.success(request, 'Ticket enviado com sucesso!')
            return redirect('chamados:enviar')
        print(form.errors)
    else:
        form = TicketForm()
    return render(request, 'chamados/enviar.html', {'form': form,
                                                    'categoria': categoria,
                                                    })

@verificar_funcionario()
@login_required
def atualizar_chamado(request, id):
    unidade = request.user.funcionario.unidade
    ticket = get_object_or_404(Ticket, pk=id, funcionario__unidade=unidade)
    funcionario = request.user.funcionario
    initial_data = {
        'unidade': unidade
    }
    if not request.user.groups.filter(name="RH") and ticket.funcionario == request.user.funcionario:
        return render(request, 'chamados/tickets_por_funcionarios.html', {'ticket': ticket} )
    elif not request.user.groups.filter(name="RH"):
        return render(request, 'chamados/listar_erro.html' )
    
    email = request.POST.get('email')
    email_corporativo = request.POST.get('email_corporativo')
    categoria = request.POST.get('categoria')

    if request.method == 'POST':
        #Ajustar para ticket que está aberto
        form = TicketUpdateForm(request.POST,  request.FILES or None, instance=ticket, initial=initial_data)
        
        print("Dados : ", form.data)
        
        if form.is_valid():
            
            form.save()
            save_it = form.save()
            save_it.save()
            subject = f"Fechamento do chamado {ticket.id} no sistema de RH"
            message = "\tSeu chamado foi finalizado no sistema de RH. \n\
\tConsulte seu chamado em http://centralrh.conti.de/\n\
------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
            print(subject)
            print(message)
            from_email = settings.EMAIL_HOST_USER

            if email_corporativo:
                to_list = [email_corporativo, settings.EMAIL_HOST_USER]
            elif email:
                to_list = [email, settings.EMAIL_HOST_USER]

            send_mail(subject, message, from_email, to_list, fail_silently=True)

            if email_corporativo:
                messages.success(request, f' E-mail enviado com sucesso para {email_corporativo}')
            elif email:
                messages.success(request, f' E-mail enviado com sucesso para {email}')
            else:
                messages.warning(request, f' Ticket atualizado porém funcionário : {ticket.funcionario.nome} não tem um e-mail.')

    
            return redirect('chamados:listar')
            
        elif ticket.finalizado and ticket.data_finalizada != None:
            messages.warning(request, 'Ticket já finalizado!')
            return redirect('chamados:listar')
        elif form.is_valid() and ticket.finalizado == False:
            messages.warning(request, 'Ticket não foi finalizado')
            return redirect('chamados:listar')
        print("Errors : ", form.errors)
    else:
        form = TicketUpdateForm()

    return render(request, 'chamados/atualizar.html', {'form': form, 'ticket': ticket})
    

@verificar_funcionario()
@login_required
def listar(request):
    if request.user.groups.filter(name="RH"):
        unidade = request.user.funcionario.unidade
        tickets = Ticket.objects.filter(funcionario__unidade=unidade).order_by('-data')
        paginator = Paginator(tickets, 10)
        page = request.GET.get('page', 1)
        tickets = paginator.get_page(page)
        return render(request, 'chamados/listar.html', {'tickets': tickets})
    else:
        funcionario = request.user.funcionario
        tickets = Ticket.objects.filter(funcionario=funcionario).order_by('-data')
        paginator = Paginator(tickets, 10)
        page = request.GET.get('page', 1)
        tickets = paginator.get_page(page)
        return render(request, 'chamados/listar.html', {'tickets': tickets})
               



