from django.forms import ModelForm, RadioSelect
from .models import Ticket, Funcionario, Unidade

from django import forms

CATEGORIA = (
            ('Benefícios', 'Benefícios'),
            ('Cargos e Salários', 'Cargos e Sálarios'),
            ('Férias', 'Férias'),
            ('Folha de Pagamento', 'Folha de Pagamento'),
            ('Ponto', 'Ponto'),
            ('Treinamento', 'Treinamento'),)

BOOL_CHOICES = ((True, 'Sim'), (False, 'Não'))

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = '__all__'

class TicketForm(forms.ModelForm):
    unidade = forms.ModelChoiceField(
        label="Unidade : ",
        queryset=Unidade.objects.all())
    funcionario = forms.ModelChoiceField(
        label="Digite seu RE : ",
        queryset=Funcionario.objects.all(),
        to_field_name="re_funcionario", 
        widget=forms.TextInput())

    class Meta:
        model = Ticket
        fields = ['unidade', 'funcionario', 'categoria', 'texto', 'nome']
        labels = {
            'nome': 'Digite o nome do funcionário : ',
            'categoria': 'Categoria : ',
            'texto': 'Descrição : ',
        }


    def clean_funcionario(self):
        print(self.cleaned_data)
        unidade = self.cleaned_data['unidade']
        funcionario = self.cleaned_data['funcionario']


        if funcionario.unidade != unidade:
            raise forms.ValidationError('Funcionário não está vinculado à essa unidade')
            
        return funcionario


class TicketUpdateForm(forms.ModelForm):
    funcionario = forms.ModelChoiceField(
        label="RE : ",
        queryset=Funcionario.objects.all(),
        to_field_name="re_funcionario", 
        widget=forms.TextInput())

    class Meta:
        model = Ticket
        fields = ['categoria', 'funcionario', 'nome', 'texto',
                  'resposta', 'data_finalizada', 'finalizado']
        labels = {
            'nome': 'Digite o nome do funcionário : ',
            'categoria': 'Categoria : ',
            'texto': 'Descrição : ',
        }
