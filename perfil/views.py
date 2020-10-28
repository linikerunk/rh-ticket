import logging
import json
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.auth import (
    authenticate, login, logout, update_session_auth_hash)
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.edit import FormView
from django.core.paginator import Paginator
from django.contrib import messages
from perfil.forms import (
    SetPasswordFormCustom,
    ResetPasswordFormCustom,
    FuncionarioForm,
    UnidadeForm,
    UnidadeUpdateForm,
    UnidadeEmailForm,
    UnidadeMenuForm,
    UnidadeGrupoForm,
    CustomAuthenticationForm,
    PasswordChangeFormCustom,
    VerificaAdmissao,
    FuncionarioCreateForm,
)
from chamados.forms import ResponsavelCategoriaForm
from .models import Funcionario, Unidade, Menu
from chamados.models import Categoria, SubCategoria, ResponsavelCategoria
from perfil.models import CentroDeCusto
from perfil.decorators import verificar_funcionario


@verificar_funcionario()
@login_required
def perfil(request):
    funcionario = Funcionario.objects.get(id=request.user.funcionario.id)
    context = {'funcionario': funcionario}
    return render(request, 'perfil/perfil.html', context)


@verificar_funcionario()
@login_required
def espelho(request):
    funcionario = Funcionario.objects.get(usuario=request.user)
    context = {'funcionario': funcionario}
    return render(request, 'perfil/espelho.html', context)


@verificar_funcionario()
@login_required
def atualizar_perfil(request, id):
    funcionario = get_object_or_404(Funcionario, pk=id)
    form = FuncionarioForm(request.POST,  request.FILES or None,
                           instance=funcionario)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            redirect('perfil:perfil')
        else:
            messages.error(request, 'Erro campos inválidos.')

    return render(request, 'perfil/perfil.html', {'form': form,
                                                  'funcionario': funcionario})


@login_required
def set_password(request):
    funcionario = request.user.funcionario
    if request.method == 'POST':
        form = PasswordChangeFormCustom(data=request.POST,  user=request.user)

        old_password = form.data["old_password"]
        admissao = str(form.data["admissao"])
        admissao_banco_dados = str(request.user.funcionario.admissao)

        if not request.user.check_password(old_password):
            messages.error(request, "O número de registro não é válido.")
            return render(request, "perfil/modificar_senha.html",
                                   {'form': form})

        elif admissao.replace('/', '') != admissao_banco_dados.replace('/', ''):
            messages.error(request, "A data de admissão está inválida")
            return render(request, "perfil/modificar_senha.html",
                          {'form': form})

        elif len(form.data['new_password1']) < 8:
            messages.error(request, "A senha precisa ser maior que 8 dígitos " /
                           "ser composta por letras e números e uma letra maiúscula ")
            return render(request, "perfil/modificar_senha.html",
                                   {'form': form})

        elif str(form.data['new_password1']) != str(form.data['new_password2']):
            messages.error(request, "As senha não se combinam.")
            return render(request, "perfil/modificar_senha.html",
                          {'form': form})

        if form.is_valid():
            form.save()
            funcionario.primeiro_acesso = False
            funcionario.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Senha alterada com sucesso!")
            return redirect('perfil:perfil')
        else:
            context = {'form': form}
            return render(request, "perfil/modificar_senha.html", context)
    else:
        form = PasswordChangeFormCustom(user=request.user)
        context = {'form': form}
        return render(request, "perfil/modificar_senha.html", context)


@login_required
def meu_logout(request):
    logout(request)
    return redirect('login')


def verifica_admissao(request):
    unidade = Unidade.objects.all()
    form = VerificaAdmissao()
    if request.method == "POST":
        form = VerificaAdmissao(request.POST or None)
        try:
            user_field = request.POST.get('id_username', None)
            admissao = request.POST.get('admissao', None)
            user = User.objects.get(username=user_field)
            funcionario = Funcionario.objects.get(usuario=user)
            if admissao == funcionario.admissao:
                login(request, user,
                      backend='Tickets.auth_backend.PasswordlessAuthBackend')
                return redirect('perfil:reset_password')
        except Exception as e:
            messages.error(
                request, 'Admissão inválida ou usuário inexistente.')
            context = {'form': form, 'unidade': unidade,
                       'mensagem': 'usuário inexistente ou campos não preenchidos.'}
            return render(request, 'perfil/verifica_senha.html', context)
    return render(request, 'perfil/verifica_senha.html', {'form': form,
                                                          'unidade': unidade})


@ verificar_funcionario()
@ login_required
def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordFormCustom(data=request.POST, user=None)
        if form.is_valid():
            password = request.POST.get('new_password1', None)
            u = User.objects.get(username__exact=request.user)
            u.set_password(password)
            u.save()
            messages.success(request, 'Senha Alterada com sucesso!')
            return redirect('chamados:enviar')
        else:
            messages.error(request, f'{form.errors}')
            return render(request, 'perfil/reset_senha.html', {'form': form})
    return render(request, 'perfil/reset_senha.html', {})


@ login_required
def unidade_admin(request):
    unidade = Unidade.objects.order_by('-id').all()
    paginator = Paginator(unidade, 10)
    page = request.GET.get('page', 1)
    obj = paginator.get_page(page)
    context = {'obj': obj}
    return render(request, 'unidade/unidade_admin.html', context)


@ login_required
def create_unidade_admin(request):
    unidade = Unidade.objects.all()
    grupo = Group.objects.all()
    form = UnidadeForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()

            messages.success(request, 'Unidade adicionada com sucesso!')
            return redirect('perfil:unidade_admin')
        else:
            messages.error(request, f'{form.errors}')
    context = {'form': form, 'unidade': unidade, 'grupo': grupo}
    return render(request, 'unidade/unidade_create.html', context)


@ login_required
def update_unidade_admin(request, id):
    unidade = get_object_or_404(Unidade, pk=id)
    context = {'unidade': unidade, }
    return render(request, 'unidade/unidade_update.html', context)


@ login_required
def update_email_admin(request, id):
    unidade = get_object_or_404(Unidade, pk=id)
    form = UnidadeEmailForm(request.POST or None, instance=unidade)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'E-mail alterado com sucesso!')
            return redirect('perfil:update_unidade_admin', id=unidade.id)
        messages.error(request, 'E-mail contém um erro!')
    context = {'unidade': unidade, 'form': form}
    return render(request, 'unidade/update_email_admin.html', context)


@ login_required
def update_menu_admin(request, id):
    unidade = get_object_or_404(Unidade, pk=id)
    menus = Menu.objects.all()
    form = UnidadeMenuForm(request.POST or None, instance=unidade)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'E-mail alterado com sucesso!')
            return redirect('perfil:update_unidade_admin', id=unidade.id)
        else:
            messages.error(request, 'Erro ao salvar os novos menus')
    context = {'unidade': unidade, 'form': form, 'menus': menus}
    return render(request, 'unidade/update_menu_admin.html', context)


@ login_required
def update_grupo_admin(request, id):
    unidade = get_object_or_404(Unidade, pk=id)
    group = Group.objects.all()

    # group_search = Group.objects.get(id=group_id)
    if request.method == 'POST':
        group_id = request.POST.get('grupo')
        user_group = request.POST.get('adiciona_funcionario')
        try:
            group_query = Group.objects.get(id=group_id)
            user = User.objects.get(username=(str(unidade.id) + user_group))
            group_query.user_set.add(user.pk)
            messages.success(request, f"Usuário ' {user.funcionario.nome} ' \
                adicionado ao grupo ' {group_query.name} ' ")
            return redirect('perfil:update_unidade_admin', id=unidade.id)
        except:
            messages.error(request, "Usuário não encontrado tente novamente.")
            context = {'group': group, 'unidade': unidade}
            return render(request, 'unidade/update_grupo_admin.html', context)
    context = {'group': group, 'unidade': unidade}
    return render(request, 'unidade/update_grupo_admin.html', context)


@ login_required
def update_categoria_admin(request, id):
    form = ResponsavelCategoriaForm(request.POST or None)
    unidade = get_object_or_404(Unidade, pk=id)
    categoria = Categoria.objects.all()
    subcategoria = SubCategoria.objects.all()
    responsavel_categoria = unidade.responsaveis_categoria.all().order_by('subcategoria__id')
    context = {'unidade': unidade, 'categoria': categoria,
               'subcategoria': subcategoria, 'form': form,
               'responsavel_categoria': responsavel_categoria}
    return render(request, 'unidade/update_categoria_admin.html', context)


@ login_required
def delete_unidade_admin(request, id):
    unidade = get_object_or_404(Unidade, pk=id)
    if request.method == "POST":
        messages.success(request,
                         f'Unidade {unidade.nome} removida com sucesso!')
        unidade.delete()
        return redirect('perfil:unidade_admin')
    context = {'unidade': unidade}
    return render(request, 'unidade/unidade_delete.html', context)


@ login_required
def delete_user_group(request, id):
    unidade = get_object_or_404(Unidade, pk=id)
    group = Group.objects.all()
    if request.method == 'POST':
        group_id = request.POST.get('grupo')
        user_group = request.POST.get('remover_funcionario')
        try:
            group_query = Group.objects.get(id=group_id)
            user = User.objects.get(username=(str(unidade.id) + user_group))
            group_query.user_set.remove(user.pk)
            messages.success(request, f"Usuário ' {user.funcionario.nome} ' \
                removido do grupo ' {group_query.name} ' ")
            return redirect('perfil:update_unidade_admin', id=unidade.id)
        except:
            messages.error(request, "Usuário não encontrado tente novamente.")
            context = {'group': group, 'unidade': unidade}
            return render(request, 'unidade/update_grupo_admin.html', context)
    context = {'group': group, 'unidade': unidade}
    return render(request, 'unidade/update_grupo_admin.html', context)


@ login_required
def add_responsavel_categoria(request, id):
    unidade = get_object_or_404(Unidade, pk=id)
    user = request.user
    categoria = Categoria.objects.all()
    subcategoria = SubCategoria.objects.all()
    responsavel_categoria = unidade.responsaveis_categoria.all().order_by('subcategoria__id')

    form = ResponsavelCategoriaForm(user, request.POST or None)

    try:
        responsavel_field = request.POST.get('responsavel')
        subcategoria_field = request.POST.get('subcategoria')
        subcategoria_field = SubCategoria.objects.get(id=subcategoria_field)
        responsavel_field = Funcionario.objects.get(
            re_funcionario=responsavel_field)
    except Exception as e:
        print(f"Funcionario não encontrado. erro : {e}")
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            try:
                responsavel_categoria = ResponsavelCategoria.objects.get(
                    responsavel=responsavel_field,
                    subcategoria=subcategoria_field)
                unidade.responsaveis_categoria.add(responsavel_categoria)
            except Exception as e:
                print(f"Valor obtido no merge não encontrado. erro : {e}")
            messages.success(request, f'{responsavel_field} está responsável  \
                pela subcategoria : {subcategoria_field}')
            context = {'unidade': unidade, 'form': form, 'categoria': categoria,
                       'subcategoria': subcategoria,
                       'responsavel_categoria': responsavel_categoria}
            return render(request, 'unidade/update_categoria_admin.html',
                          context)
        else:
            messages.error(request, 'Funcionário inexistente, \
            certifique se o regitro está correto.')
    context = {'unidade': unidade, 'form': form, 'categoria': categoria,
               'subcategoria': subcategoria,
               'responsavel_categoria': responsavel_categoria}
    return render(request, 'unidade/update_categoria_admin.html', context)


def remove_responsavel_categoria(request, id):
    unidade = get_object_or_404(Unidade, pk=id)
    subcategoria = SubCategoria.objects.all()
    responsavel_categoria = unidade.responsaveis_categoria.all().order_by('subcategoria__id')
    if request.method == 'POST':
        remove_responsavel = request.POST.get('remove_responsavel')
        remove_subcategoria = request.POST.get('remove_subcategoria')
        try:
            user = User.objects.get(
                username=(str(unidade.id) + remove_responsavel))
            subcategoria_object = SubCategoria.objects.get(
                id=remove_subcategoria)
            responsavel_categoria = ResponsavelCategoria.objects.filter(
                responsavel=user.funcionario,
                subcategoria=remove_subcategoria)
            # unidade.responsaveis_categoria.remove(responsavel_categoria.id)
            responsavel_categoria.delete()
            messages.success(request, f"Usuário ' {user.funcionario.nome} ' \
               foi removida da subcategoria' {subcategoria_object}' ")
            return redirect('perfil:update_categoria_admin', id=unidade.id)
        except:
            messages.error(request, "Usuário não encontrado tente novamente.")
            context = {'subcategoria': subcategoria, 'unidade': unidade,
                       'responsavel_categoria': responsavel_categoria}
            return render(request, 'unidade/update_categoria_admin.html', context)
    context = {'subcategoria': subcategoria, 'unidade': unidade,
               'responsavel_categoria': responsavel_categoria}
    return render(request, 'unidade/update_categoria_admin.html', context)


@ verificar_funcionario()
@ login_required
def adicionar_funcionario(request):
    unidade = Unidade.objects.all()
    centro_de_custo = CentroDeCusto.objects.all()
    form = FuncionarioCreateForm(request.POST or None)
    if request.method == "POST":
        nome = request.POST.get('nome', None)
        if form.is_valid():
            messages.success(request, f'Funcionário : {nome} adicionado com sucesso!')
            form.save()
            return redirect('perfil:adicionar_funcionario')
        else:
            messages.error(request, f"{form.errors}")
    context = {'unidade': unidade, 'centro_de_custo': centro_de_custo}
    return render(request, 'rh/adiciona_funcionario.html', context)


@ verificar_funcionario()
@ login_required
def listar_funcionario(request):
    obj = Funcionario.objects.filter(unidade="1")
    context = {'obj': obj}
    return render(request, 'rh/listar_funcionario.html', context)


@ verificar_funcionario()
@ login_required
def editar_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, pk=id)
    unidade = Unidade.objects.all()
    centro_de_custo = CentroDeCusto.objects.all()
    if request.method == "POST":
        form = FuncionarioEditForm(request.POST or None, instance=unidade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Funcionário editado com sucesso!')
            return redirect('perfil:listar_funcionario')
    context = {'funcionario': funcionario, 'unidade': unidade,
               'centro_de_custo': centro_de_custo}
    return render(request, 'rh/editar_funcionario.html', context)


class Login(auth_views.LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'perfil/login.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unidade = Unidade.objects.all()
        re = Funcionario.objects.filter(unidade=unidade)
        context.update({'unidade': unidade,
                        're': re, })
        return context