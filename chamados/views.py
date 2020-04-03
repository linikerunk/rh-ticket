from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User # Chamados
from django.core.mail import send_mail, send_mass_mail
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Ticket, Funcionario
from .forms import TicketForm, TicketUpdateForm, FuncionarioForm

# Create your views here.

def selecionar_unidade(request):
    context = {}
    return render(request, 'chamados/selecionar-unidade.html', context)
    

def funcionario_ajax(request, id):
    re_func = request.GET.get('re_func')
    funcionario  = Funcionario.objects.filter(re_funcionario=re_func).first()
    response = {}
    if funcionario:
        response = {"nome": funcionario.nome, 'email': funcionario.email}
    return JsonResponse(response)
        

def enviar(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        email = request.POST.get('email')
        texto = request.POST.get('texto')
        categoria = request.POST.get('categoria')
        if form.is_valid():
            form.save()
            save_it = form.save()
            save_it.save()
            subject = categoria
            message = texto
            from_email = settings.EMAIL_HOST_USER
            recipient_list = ['pedro.melo@continental.com', 
            'andreia.nogueira@continental.com', 'fabiana.carvalho@continental.com']
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)
            messages.success(request, 'Ticket enviado com sucesso!')
            return redirect('chamados:enviar')
    else:
        form = TicketForm()
    return render(request, 'chamados/enviar.html', {'form': form})

@login_required
def atualizar_chamado(request, id):
    unidade = request.user.perfil.unidade
    ticket = get_object_or_404(Ticket, pk=id, funcionario__unidade=unidade)
    initial_data = {
        'unidade': unidade
    }
    email = request.POST.get('email')
    categoria = request.POST.get('categoria')
    texto = request.POST.get('texto')

    if request.method == 'POST':
        form = TicketUpdateForm(request.POST, instance=ticket, initial=initial_data)
        if form.is_valid() and ticket.finalizado == True and ticket.data_finalizada == None:
            if not email or not categoria:
                messages.error(request, 'Nenhum campo pode estar vazio.')
                return render(request, 'chamados/atualizar.html', {'form': form, 'ticket': ticket})
            # try:
            #     print(email)
            #     print(resposta)
            #     validate_email(email)
            # except:
            #     messages.error(request, 'E-mail Inválido.')
            #     return render(request, 'chamados/atualizar.html', {'form': form, 'ticket': ticket})
            form.save()
            save_it = form.save()
            save_it.save()
            subject = categoria
            message = texto
            from_email = settings.EMAIL_HOST_USER
            to_list = [email, settings.EMAIL_HOST_USER]

            send_mail(subject, message, from_email, to_list, fail_silently=True)
            messages.success(request, f' E-mail enviado com sucesso para {email}')
            return redirect('chamados:listar')
            
        elif ticket.finalizado and ticket.data_finalizada != None:
            messages.warning(request, 'Ticket já finalizado!')
            return redirect('chamados:listar')
        elif form.is_valid() and ticket.finalizado == False:
            messages.warning(request, 'Ticket não foi finalizado')
            return redirect('chamados:listar')
    else:
        form = TicketUpdateForm()

    return render(request, 'chamados/atualizar.html', {'form': form, 'ticket': ticket})

@login_required
def listar(request):
    unidade = request.user.perfil.unidade
    tickets = Ticket.objects.filter(funcionario__unidade=unidade).order_by('-data')
    
    paginator = Paginator(tickets, 10)
    page = request.GET.get('page', 1)
    tickets = paginator.get_page(page)
    
    return render(request, 'chamados/listar.html', {'tickets': tickets})       

def login(request):
    context = {}
    return render(request, 'home/login.html', context)

@login_required
def meu_logout(request):
    logout(request)
    return redirect('login')