from django.forms import ModelForm, RadioSelect
from django.core.exceptions import ValidationError
from django.forms.widgets import PasswordInput, TextInput, CheckboxSelectMultiple, SelectMultiple
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    PasswordChangeForm,
    AuthenticationForm,
    UsernameField,
    SetPasswordForm,
)
from django.contrib.auth import authenticate
from .models import Funcionario, Unidade, Menu
from django import forms


# Create your models here.

class FuncionarioForm(forms.ModelForm):

    class Meta:
        model = Funcionario
        fields = ['re_funcionario', 'nome', 'ramal',
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

class FuncionarioCreateForm(forms.ModelForm):

    class Meta:
        model = Funcionario
        fields = ['re_funcionario', 'nome', 'admissao', 'email', 'email_corporativo',
                  'telefone', 'ramal', 'unidade', 'centro_de_custo_link',]


class FuncionarioEditForm(forms.ModelForm):

    class Meta:
        model = Funcionario
        fields = ['re_funcionario', 'nome', 'admissao', 'demissao', 'email',
         'email_corporativo', 'telefone', 'ramal', 'unidade',
         'centro_de_custo_link',]


class UnidadeForm(forms.ModelForm):
    menu = forms.ModelMultipleChoiceField(
        queryset=Menu.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True)

    class Meta:
        model = Unidade
        fields = ['nome', 'email', 'menu', 'grupo']

        label = {
            'nome': 'Nome:',
            'email': 'E-mail:',
            'menu': 'Menu:',
            'grupo': 'Grupo',
        }

    def __init__(self, *args, **kwargs):
        super(UnidadeForm, self).__init__(*args, **kwargs)
        self.fields["menu"].widget = CheckboxSelectMultiple()
        self.fields["menu"].queryset = Menu.objects.all()

    def clean_grupo(self):
        grupo = self.cleaned_data['grupo']
        if not grupo:
            raise forms.ValidationError("Você deve informar os Grupos "
                                        "existentes.")
        return grupo


class UnidadeUpdateForm(forms.ModelForm):
    menu = forms.ModelMultipleChoiceField(
        queryset=Menu.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True)

    def __init__(self, *args, **kwargs):
        super(UnidadeUpdateForm, self).__init__(*args, **kwargs)
        self.fields["menu"].widget = CheckboxSelectMultiple()
        self.fields["menu"].queryset = Menu.objects.all()

    class Meta:
        model = Unidade
        fields = ['nome', 'email', 'menu']

        label = {
            'nome': 'Nome:',
            'email': 'E-mail:',
            'menu': 'Menu:'
        }


class UnidadeEmailForm(forms.ModelForm):
    class Meta:
        model = Unidade
        fields = ['email', ]

        label = {'email': 'E-mail:'}


class UnidadeGrupoForm(forms.ModelForm):
    class Meta:
        model = Unidade
        fields = ['grupo']

        label = {'grupo': 'Grupo'}


class UnidadeMenuForm(forms.ModelForm):
    menu = forms.ModelMultipleChoiceField(
        queryset=Menu.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True)

    def __init__(self, *args, **kwargs):
        super(UnidadeMenuForm, self).__init__(*args, **kwargs)
        self.fields["menu"].widget = CheckboxSelectMultiple()
        self.fields["menu"].queryset = Menu.objects.all()

    class Meta:
        model = Unidade
        fields = ['menu']

        label = {'menu': 'Menu:'}


class UnidadeCategoriaForm(forms.ModelForm):

    class Meta:
        model = Unidade
        fields = ['responsaveis_categoria']

        label = {'responsaveis_categoria': 'Responsável pela Categoria:'}


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(
        attrs={'class': 'validate', 'placeholder': 'O Registro de usuário é conhecido como RE também.'}))

    password = forms.CharField(
        label="Senha :",
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
            self.user_cache = authenticate(
                self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class SetPasswordFormCustom(SetPasswordForm):
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


class VerificaAdmissao(forms.Form):

    re_funcionario = forms.CharField(label=("Registro do Funcionário : "),
                                     widget=TextInput(attrs={'class': 'validate', 'name': 'id_username',
                                                             'placeholder': 'Digite o Registro de Funcionário'}))

    id_username = forms.CharField(widget=TextInput())

    admissao = forms.CharField(label=("Digite sua data da admissão :"),
                               widget=forms.TextInput(
        attrs={'placeholder': 'Digite a data de sua Admissão'})
    )

    class Meta:
        model = User
        fields = ['re_funcionario', 'id_username', 'admissao']

    # def clean(self):
    #     re_funcionario = self.cleaned_data["re_funcionario"]
    #     try:
    #         user = Funcionario.objects.get(username=re_funcionario)
    #         print("Login")
    #         if self.admissao == user.admissao:
    #             print("Admissão são iguais!")
    #         else:
    #             print("Não confere as admissões...")
    #     except Exception as e:
    #         print("funcionário inexistente")


class ResetPasswordFormCustom(SetPasswordForm):
    print("Reset PasswordChangeFormCustom")
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
        widget=forms.TextInput(attrs={'placeholder': 'Digite a data de sua Admissão'}))

    old_password = forms.CharField(
        label=("Número de Registro : "),)

    field_order = ['old_password', 'admissao',
                   'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError(
                'Erro', code='invalid',
            )
        return old_password
