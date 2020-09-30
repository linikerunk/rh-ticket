# -*- coding: utf-8 -*-
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from django.forms import ModelForm, RadioSelect, ModelChoiceField

from .models import (
    Ticket,
    Categoria,
    SubCategoria,
    HistoricoTicket,
    ResponsavelCategoria,
)
from perfil.models import Funcionario, Unidade

from django import forms


BOOL_CHOICES = ((True, 'Sim'), (False, 'Não'))


class TicketForm(forms.ModelForm):
    
    upload_arquivo = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'multiple': True}), required=False, label="Anexar Arquivo : ")


    class Meta:
        model = Ticket
        fields = [ 'categoria', 'subcategoria', 'data_finalizada',
        'texto', 'resposta', 'upload_arquivo']
        labels = {
            'categoria': 'Categoria : ',
            'subcategoria': 'Subcategoria : ',
            'texto': 'Descrição : ',
            'upload_arquivo': 'Anexar arquivos : '
        }
        
        widgets={
            'texto': forms.Textarea(
                attrs={'placeholder': 'Informe um telefone e/ou e-mail para retorno do chamado',
                       'rows': 5}),  
        }


class TicketUpdateForm(forms.ModelForm):
    # funcionario = forms.ModelChoiceField(
    #     label="Funcionario",
    #     queryset= User.objects.all(),
    #     to_field_name="funcionario", 
    #     widget=forms.TextInput())
    
    upload_arquivo = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'multiple': True}), required=False, label="Anexar Arquivo : ")
    

    class Meta:
        model = Ticket
        fields = ['resposta', 'data_finalizada', 'upload_arquivo', 'finalizado']
        labels = {
            'categoria': 'Categoria : ',
            'subcategoria': 'Subcategoria : ',
            'texto': 'Descrição : ',
        }


class ResponsavelCategoriaForm(forms.ModelForm):
    responsavel = forms.ModelChoiceField(queryset=Funcionario.objects.all(),
    required=False)

    class Meta:
        model = ResponsavelCategoria
        fields = '__all__'
        labels = {
            'responsavel': 'Responsável : ',
            'subcategoria': 'Subcategoria : ',
        }





 