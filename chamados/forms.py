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
        fields = ['categoria', 'subcategoria', 'data_finalizada',
                  'texto', 'resposta', 'upload_arquivo']
        labels = {
            'categoria': 'Categoria : ',
            'subcategoria': 'Subcategoria : ',
            'texto': 'Descrição : ',
            'upload_arquivo': 'Anexar arquivos : '
        }

        widgets = {
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
        fields = ['resposta', 'data_finalizada',
                  'upload_arquivo', 'finalizado']
        labels = {
            'categoria': 'Categoria : ',
            'subcategoria': 'Subcategoria : ',
            'texto': 'Descrição : ',
        }


class ResponsavelCategoriaForm(forms.ModelForm):
    responsavel = forms.IntegerField(label="Responsável")


    class Meta:
        model = ResponsavelCategoria
        fields = '__all__'
        labels = {
            'responsavel': 'Responsável : ',
            'subcategoria': 'Subcategoria : ',
        }
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ResponsavelCategoriaForm, self).__init__(*args, **kwargs)

    def clean_responsavel(self):
        unidade = self.user.funcionario.unidade.id
        responsavel_concatenado = str(unidade) + str(
                                    self.cleaned_data.get('responsavel'))
        try:
            usuario = User.objects.get(username=responsavel_concatenado)
            print(usuario)
            self.cleaned_data['responsavel'] = Funcionario.objects.get(
                usuario=usuario)
            self.clean_responsavel = self.cleaned_data['responsavel']   
        except Exception as e:
            print(f"Erro na query realizada: {e}")
            self.clean_responsavel = None
        
        return self.clean_responsavel




 
