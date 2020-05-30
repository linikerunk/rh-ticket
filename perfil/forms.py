from django.forms import ModelForm, RadioSelect
from .models import Funcionario, Perfil, Unidade
from django import forms


# Create your models here.

class FuncionarioForm(forms.ModelForm):

    class Meta:
        model = Funcionario
        fields = ['re_funcionario', 'nome', 'cpf', 'centro_de_custo', 'ramal',
        'telefone', 'email_corporativo', 'email', 'unidade']
        
        label = {
            're_funcionario': 'RE do Funcionário : ',
            'nome': 'Nome do Funcionário : ',
            'cpf': 'CPF : ',
            'centro_de_custo': 'Centro de Custo : ',
            'ramal': 'Ramal : ',
            'telefone': 'Telefone : ',
            'email_corporativo': 'Email Corporativo : ',
            'email': 'Email do Funcionário : ',
            'unidade': 'Unidade : ',

        }


class PerfilForm(forms.ModelForm):

    class Meta:
        model = Perfil
        fields = '__all__'


class UnidadeForm(forms.ModelForm):

    class Meta:
        model = Unidade
        fields = ['nome',]
    
