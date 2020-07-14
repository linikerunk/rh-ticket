# -*- coding: utf-8 -*-
from django.utils import timezone
from datetime import datetime

from django.forms import ModelForm, RadioSelect
from .models import Ticket, Categoria, SubCategoria, HistoricoTicket
from perfil.models import Funcionario, Unidade

from django import forms


BOOL_CHOICES = ((True, 'Sim'), (False, 'Não'))


class TicketForm(forms.ModelForm):

    
    upload_arquivo = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'multiple': True}), required=False, label="Anexar Arquivo : ")


    class Meta:
        model = Ticket
        fields = ['categoria', 'subcategoria', 'funcionario', 'data_finalizada',
        'texto', 'resposta', 'upload_arquivo', 'finalizado']
        labels = {
            'categoria': 'Categoria : ',
            'subcategoria': 'Subcategoria : ',
            'texto': 'Descrição : ',
            'upload_arquivo': "Anexar arquivos : "
        }
        
        widgets={
            'texto': forms.Textarea(
                attrs={'placeholder': 'Informe um telefone e/ou e-mail para retorno do chamado',
                       'rows': 5}),  
        }


    def save(self, commit=True):
        instance = super(TicketForm, self).save(commit=False)
        historico_ticket = HistoricoTicket.objects.create(
                           data_mensagem = timezone.now(),
                           mensagem = instance.resposta,
                           ticket = instance,
                           funcionario = instance.funcionario)
        historico_ticket.save()
        print("criou um historico para isso...")
        self.resposta = ' '
        print("resposta : ", self.resposta)
        instance.funcionario = request.user
        instance.finalizado = False
        instance.save()
        print('instance : ', instance.resposta)
        print("Salvou o ticket tbm lindao")
        print("Criou um ticket novo")
        return instance

    


class TicketUpdateForm(forms.ModelForm):
    # funcionario = forms.ModelChoiceField(
    #     label="RE : ",
    #     queryset=Funcionario.objects.all(),
    #     to_field_name="re_funcionario", 
    #     widget=forms.TextInput())
    
    upload_arquivo = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'multiple': True}), required=False, label="Anexar Arquivo : ")
    

    class Meta:
        model = Ticket
        fields = ['resposta', 'data_finalizada', 'finalizado', 'upload_arquivo']
        labels = {
            'categoria': 'Categoria : ',
            'subcategoria': 'Subcategoria : ',
            'texto': 'Descrição : ',
        }

    def save(self, commit=True):
        instance = super(TicketUpdateForm, self).save(commit=True)
        historico_ticket = HistoricoTicket.objects.create(
                           data_mensagem = timezone.now(),
                           mensagem = instance.resposta,
                           ticket = instance,
                           funcionario = instance.funcionario)
        historico_ticket.save()
        print("criou um historico para isso...")
        self.resposta = ' '
        print("resposta : ", self.resposta)
        instance.save()
        print('instance : ', instance.resposta)
        print("Salvou o ticket tbm lindao")
        print("estou fazendo duas vezes isso aqui ?")
        return instance


 