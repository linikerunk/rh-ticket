from django.forms import ModelForm, RadioSelect, PasswordInput
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import Funcionario, Unidade
from django import forms


# Create your models here.

class FuncionarioForm(forms.ModelForm):

    class Meta:
        model = Funcionario
        fields = ['re_funcionario', 'nome', 'centro_de_custo', 'ramal',
        'telefone', 'email_corporativo', 'email', 'unidade']
        
        label = {
            're_funcionario': 'RE do Funcionário : ',
            'nome': 'Nome do Funcionário : ',
            'centro_de_custo': 'Centro de Custo : ',
            'ramal': 'Ramal : ',
            'telefone': 'Telefone : ',
            'email_corporativo': 'Email Corporativo : ',
            'email': 'Email do Funcionário : ',
            'unidade': 'Unidade : ',

        }


class UnidadeForm(forms.ModelForm):

    # unidade = forms.ModelChoiceField(
    #     label="Unidade : ",
    #     queryset=Unidade.objects.all(),
    #     to_field_name="nome")

    class Meta:
        model = Unidade
        fields = ['nome',]


class CustomAuthenticationForm(AuthenticationForm):

    username = UsernameField(
        label= ("Usuário (RE) :"), 
        widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label=("Senha: "),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )


    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)


    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        concatenar = self.cleaned_data.get('concatenar') 

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    
    def get_user(self):
        return self.user_cache

    
