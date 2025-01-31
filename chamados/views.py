# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, Group  # Chamados
from django.core.mail import send_mail, send_mass_mail
from django.core import serializers
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils import timezone
from django.template import Context
from django.core import serializers

from .models import Ticket, Categoria, SubCategoria, HistoricoTicket
from perfil.models import Funcionario, Unidade
from .forms import TicketForm, TicketUpdateForm
from perfil.forms import FuncionarioForm, ResetPasswordFormCustom
from perfil.decorators import *
import json


def funcionario_login_reset_ajax(request, id):
    re_funcionario = request.GET.get('username')
    response = {'re_funcionario': re_funcionario}
    return JsonResponse(response)


def show_user_by_group_ajax(request, id):
    unidade = request.GET.get('unidade', None)
    user_belong_group = Funcionario.objects.filter(
        unidade=unidade).filter(usuario__groups=id)
    user_group = [item for item in user_belong_group]
    return JsonResponse(serializers.serialize('json', user_group), safe=False)


def funcionario_login_ajax(request, id):
    re_funcionario = request.GET.get('funcionario-login')
    response = {'re_funcionario': re_funcionario}
    return JsonResponse(response)


def verifica_admissao_ajax(request, id):
    re_funcionario = request.GET.get('funcionario-login')
    unidade = request.GET.get('unidade')
    unidade = Unidade.objects.get(nome=unidade).id()
    print("unidade : ", unidade)
    response = {'unidade': unidade}
    return JsonResponse(response)


def verificar_senha_ajax(request, id):
    try:
        campo_usuario = request.GET.get('username')
        campo_admissao = request.GET.get('admissao')
        usuario = User.objects.get(username=campo_usuario)
        funcionario = Funcionario.objects.get(usuario=usuario)
        usuario, admissao = funcionario.usuario, funcionario.admissao
        usuario = str(usuario)
    except User.DoesNotExist:
        print("Usuário inexistente.")
        response = {'erro': 'Usuário inexistente.'}
        return JsonResponse(response)
    if campo_admissao == funcionario.admissao:
        form = ResetPasswordFormCustom(data=request.POST, user=None)
        form.user = usuario
        print("Form : ", form.data)
        print("FormField : ", form.fields)
        if form.is_valid():
            form.save()
            return redirect('chamados:enviar')
        print("Campos são iguais")
        response = {'usuario': usuario,
                    'campo_admissao': campo_admissao}
        return JsonResponse(response)
    else:
        print("Campos são diferentes..")
        print(f"Data é {funcionario.admissao}")
        response = {'erro': 'Data admissão são diferentes..'}
        return JsonResponse(response)


def funcionario_ajax(request, id):
    re_func = request.GET.get('re_func')
    funcionario = Funcionario.objects.filter(re_funcionario=re_func).first()
    response = {}
    if funcionario:
        response = {"nome": funcionario.nome, 'email': funcionario.email}
    return JsonResponse(response)


def carregar_subcategorias(request, id):
    subcategoria = SubCategoria.objects.filter(categoria=id)
    data = serializers.serialize("json", subcategoria, fields=('id', 'nome'))
    response = {'data': data}
    return JsonResponse(response, safe=False)


@verificar_funcionario()
@login_required
def enviar(request):
    categoria = Categoria.objects.all()
    unidade = request.user.funcionario.unidade
    funcionario = request.user.funcionario
    if request.method == 'POST':
        form = TicketForm(request.POST,  request.FILES or None)
        email = request.POST.get('email')
        categoria_id = request.POST.get('categoria')
        categoria = Categoria.objects.get(id=categoria_id)
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
            message = f"\tCategoria : {categoria}\n\tSubcategoria : {subcategoria}\n\t\
RE : {funcionario.re_funcionario}\n\tCDC: {funcionario.centro_de_custo_link}\n\tNome : {funcionario.nome}\n\tDescrição : {texto}\n\
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
            unidade = Unidade.objects.get(id=unidade.id)
            responsavel_subcategoria = unidade.responsaveis_categoria.filter(
                subcategoria=subcategoria)
            emails_funcionario_responsavel = []
            for funcionario in responsavel_subcategoria:
                emails_funcionario_responsavel.append(funcionario.responsavel.email_corporativo)
            from_email = unidade.email
            recipient_list = emails_funcionario_responsavel
            print(recipient_list)
            send_mail(subject, message, from_email,
                      recipient_list, fail_silently=True)
            messages.success(request, 'Ticket enviado com sucesso!')
            return redirect('chamados:enviar')
        print(form.errors)
        print(form.data)
    else:
        form = TicketForm()
    return render(request, 'chamados/enviar.html', {'form': form,
                                                    'categoria': categoria, })


@verificar_funcionario()
@login_required
def finalizar_chamado(request, id):
    unidade = request.user.funcionario.unidade
    ticket = get_object_or_404(Ticket, pk=id, funcionario__unidade=unidade)
    funcionario = request.user.funcionario
    historico = HistoricoTicket.objects.filter(ticket__id=ticket.id)
    initial_data = {'unidade': unidade}

    if request.method == 'POST':
        if not request.user.groups.filter(name="RH") or ticket.funcionario == request.user.funcionario:
            form = TicketUpdateForm(
                request.POST,  request.FILES or None, instance=ticket, initial=initial_data)

            if form.is_valid():
                historico_ticket = HistoricoTicket.objects.create(
                    data_mensagem=timezone.now(),
                    mensagem=form.instance.resposta,
                    ticket_id=form.instance.id,
                    funcionario=request.user.funcionario)
                historico_ticket.save()

                subject = f"Resposta do funcionário {ticket.funcionario.nome} do registro {ticket.funcionario.re_funcionario}."
                message = f"\t Resposta : {ticket.resposta} \n \
 ------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
                form.instance.resposta = ''
                form.save()
                save_it = form.save()
                save_it.save()
                print(subject)
                print(message)
            if ticket.funcionario.email_corporativo is not None:
                from_email = unidade.email
                to_list = [ticket.funcionario.email_corporativo, unidade.email]
            elif ticket.funcionario.email is not None:
                from_email = unidade.email
                to_list = [ticket.funcionario.email, unidade.email]
            else:
                form.to_list = ['', unidade.email]
                messages.success(
                    request, f'Ticket respondido com sucesso, mas funcionário não tem e-mail')
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)
            messages.success(request, 'Chamado respondido com sucesso.')
            messages.warning(
                request, 'Alerta: o disparo de e-mail é restrito a endereços corporativos.')

            return render(request, 'chamados/tickets_por_funcionarios.html', {'ticket': ticket,
                                                                              'historico': historico})
        elif not request.user.groups.filter(name="RH"):
            return render(request, 'chamados/listar_erro.html')

        email = request.POST.get('email')
        email_corporativo = request.POST.get('email_corporativo')
        categoria = request.POST.get('categoria')
        # Ajustar para ticket que está aberto
        form = TicketUpdateForm(
            request.POST,  request.FILES or None, instance=ticket, initial=initial_data)

        if form.is_valid():
            historico_ticket = HistoricoTicket.objects.create(
                data_mensagem=timezone.now(),
                mensagem=form.instance.resposta,
                ticket_id=form.instance.id,
                funcionario=request.user.funcionario)
            historico_ticket.save()
            form.instance.resposta = ''
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

            if ticket.funcionario.email_corporativo is not None:
                from_email = settings.EMAIL_HOST_USER
                to_list = [ticket.funcionario.email_corporativo,
                           settings.EMAIL_HOST_USER]
                print("email : ", ticket.funcionario.email_corporativo)
            elif ticket.funcionario.email is not None:
                from_email = settings.EMAIL_HOST_USER
                to_list = [ticket.funcionario.email, settings.EMAIL_HOST_USER]
            else:
                to_list = ['', settings.EMAIL_HOST_USER]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            if ticket.funcionario.email_corporativo and ticket.finalizado:
                messages.success(request, 'Chamado finalizado com sucesso.')
                messages.warning(
                    request, 'Alerta: o disparo de e-mail é restrito a endereços corporativos.')

            elif ticket.funcionario.email and ticket.finalizado:
                messages.success(request, 'Chamado finalizado com sucesso.')
                messages.warning(
                    request, 'Alerta: o disparo de e-mail é restrito a endereços corporativos.')

            elif ticket.funcionario.email_corporativo or ticket.funcionario.email and ticket.finalizado == False:
                messages.success(request, 'Chamado respondido com sucesso.')
                messages.warning(
                    request, 'Alerta: o disparo de e-mail é restrito a endereços corporativos.')
            else:
                messages.success(request, 'Chamado finalizado com sucesso.')
                messages.warning(
                    request, 'Alerta: o disparo de e-mail é restrito a endereços corporativos.')

            return redirect('chamados:listar')

        elif ticket.finalizado and ticket.data_finalizada != None:
            messages.warning(request, 'Ticket já finalizado!')
            print('Ticket já finalizado!')
            return redirect('chamados:listar')

        elif form.is_valid() and ticket.finalizado == False:
            messages.warning(request, 'Ticket respondido')
            print('Ticket não foi finalizado')
            return redirect('chamados:listar')

        print(f"Forms errors : {form.errors}")
        print(f"Forms data : {form.data}")

    form = TicketUpdateForm(
        request.POST,  request.FILES or None, instance=ticket, initial=initial_data)
    return render(request, 'chamados/tickets_por_funcionarios.html', {'form': form, 'ticket': ticket, 'historico': historico})


@verificar_funcionario()
@login_required
def listar(request):
    if request.user.groups.filter(name="RH"):
        unidade = request.user.funcionario.unidade
        tickets = Ticket.objects.filter(
            funcionario__unidade=unidade).order_by('-data')
        paginator = Paginator(tickets, 10)
        page = request.GET.get('page', 1)
        obj = paginator.get_page(page)
        return render(request, 'chamados/listar.html', {'tickets': tickets,
                                                        'obj': obj})
    else:
        funcionario = request.user.funcionario
        tickets = Ticket.objects.filter(
            funcionario=funcionario).order_by('-data')
        paginator = Paginator(tickets, 10)
        page = request.GET.get('page', 1)
        obj = paginator.get_page(page)
        return render(request, 'chamados/listar.html', {'tickets': tickets,
                                                        'obj': obj})
