# -*- coding: utf-8 -*-

from django.forms import ModelForm, RadioSelect
from .models import Ticket, Categoria, SubCategoria
from perfil.models import Funcionario, Unidade

from django import forms


BOOL_CHOICES = ((True, 'Sim'), (False, 'Não'))


class TicketForm(forms.ModelForm):

    # unidade = forms.ModelChoiceField(
    #     label="Unidade : ",
    #     queryset=Unidade.objects.all(),
    #     to_field_name="nome")

    # funcionario = forms.ModelChoiceField(
    #     label="RE : ",
    #     queryset=Funcionario.objects.all(),
    #     to_field_name="re_funcionario", 
    #     widget=forms.TextInput())
    
    categoria = forms.ModelChoiceField(
        label="Categoria : ",
        queryset=Categoria.objects.all(),
        to_field_name="nome")
    

    upload_arquivo = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'multiple': True}), required=False, label="Anexar Arquivo : ")


    class Meta:
        model = Ticket
        fields = ['categoria', 'subcategoria', 'texto',
        'upload_arquivo']
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


    def clean_funcionario(self):
        unidade = self.cleaned_data['unidade']
        funcionario = self.cleaned_data['funcionario']


        if funcionario.unidade != unidade:
            raise forms.ValidationError('Funcionário não está vinculado à essa unidade')
            
        return funcionario


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
