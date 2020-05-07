from django.forms import ModelForm, RadioSelect
from .models import Funcionario, Perfil, Unidade
from django import forms


# Create your models here.

class FuncionarioForm(forms.ModelForm):

    class Meta:
        model = Funcionario
        fields = ['re_funcionario', 'nome', 'centro_de_custo', 'ramal',
        'email_corporativo', 'email', 'unidade']
        label = {
            're_funcionario': 'RE do Funcionário : ',
            'nome': 'Nome do Funcionário : ',
            'centro_de_custo': 'Centro de Custo : ',
            'ramal': 'Ramal : ',
            'email': 'Email do Funcionário : '
        }


class PerfilForm(forms.ModelForm):

    class Meta:
        model = Perfil
        fields = '__all__'


class UnidadeForm(forms.ModelForm):

    class Meta:
        model = Unidade
        fields = ['nome',]
    
