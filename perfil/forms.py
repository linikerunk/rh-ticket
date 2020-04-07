from django.forms import ModelForm, RadioSelect
from .models import Funcionario, Perfil, Funcionario
from django import forms


# Create your models here.

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = '__all__'
        label = {
            're_funcionario': 'RE do Funcionário : ',
            'nome': 'Nome do Funcionário : ',
            'centro_de_custo': 'Centro de Custo : ',
            'ramal': 'Ramal : ',
            'email': 'Email do Funcionário : ',
            'perfil__unidade': 'Unidade : '
        }
    
