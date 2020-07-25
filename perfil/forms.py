from django.forms import ModelForm, RadioSelect
from django.core.exceptions import ValidationError
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
PasswordChangeForm,
AuthenticationForm,
UsernameField,
SetPasswordForm,
)
from django.contrib.auth import authenticate
from .models import Funcionario, Unidade
from django import forms


# Create your models here.

class FuncionarioForm(forms.ModelForm):

    class Meta:
        model = Funcionario
        fields = ['re_funcionario', 'nome', 'centro_de_custo_link', 'ramal',
        'telefone', 'email_corporativo', 'email', 'unidade', 'termo_dados']
        
        label = {
            're_funcionario': 'RE do Funcionário : ',
            'nome': 'Nome do Funcionário : ',
            'centro_de_custo_link': 'Centro de Custo : ',
            'ramal': 'Ramal : ',
            'telefone': 'Telefone : ',
            'email_corporativo': 'Email Corporativo : ',
            'email': 'Email do Funcionário : ',
            'unidade': 'Unidade : ',
            'termo_dados': 'Termo de Consentimento',
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
    username = forms.CharField(widget=TextInput(
        attrs={'class':'validate','placeholder': 'O Registro de usuário é conhecido como RE também.'}))

    password = forms.CharField(
        label= "Senha :",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
        'placeholder': 'Caso seja seu primeiro acesso, utilizar o número do seu registro.'}),
    )


    def __init__(self, request=None, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.request = request
        self.user_cache = None


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


class SetPasswordFormCustom(SetPasswordForm):
    print("Set PasswordForm")
    error_messages = {
        'password_mismatch': ('A senhas não se combinam..'),
    }

    new_password1 = forms.CharField(
        label=("Nova Senha"),
    )

    new_password2 = forms.CharField(
        label=("Confirmação de Nova Senha"),
    )


    def clean(self):
        unidade = self.cleaned_data.get('unidade')
        registro = self.cleaned_data.get('registro')
        return self.cleaned_data


class PasswordChangeFormCustom(PasswordChangeForm):
    admissao = forms.CharField(
        label=("Digite sua data da admissão :"),
        widget=forms.TextInput(attrs={'placeholder':'Digite a data de sua Admissão'})
        
    )

    old_password = forms.CharField(
        label=("Número de Registro : "),
    )


    field_order = ['old_password', 'admissao', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def clean_old_password(self):
        
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError(
              'Teste', code='invalid',
            )
        return old_password


    
