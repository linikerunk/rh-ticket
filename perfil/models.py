from django.db import models
from datetime import datetime
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings

now = datetime.now()

TERMO = (
     ("1", "Alteração"),
    ("2", "Exclusão"),
)



class Unidade(models.Model):
    nome = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.nome


class Funcionario(models.Model):
    re_funcionario = models.CharField(max_length=9, verbose_name="RE")
    nome = models.CharField(max_length=55, verbose_name="Funcionário :")
    centro_de_custo = models.CharField(max_length=10)
    admissao = models.CharField(max_length=20, blank=True, verbose_name="Data de Admissão : ", default="")
    demissao = models.CharField(max_length=20, blank=True, verbose_name="Data de Demissão : ", default="")
    ramal = models.CharField(max_length=9, blank=True, verbose_name="Ramal", default="")
    telefone = models.CharField(max_length=11, blank=True, verbose_name="Telefone", default="")
    email_corporativo = models.EmailField(max_length=254, verbose_name="Email Corporativo", blank=True, default="")
    email = models.EmailField(max_length=254, verbose_name="Email Pessoal", blank=True, default="")
    primeiro_acesso = models.BooleanField(verbose_name="Primeiro Acesso", default=True)
    unidade = models.ForeignKey(Unidade, related_name="funcionarios", on_delete=models.PROTECT)
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    termo_dados = models.CharField(verbose_name="Termo de Consentimento", max_length=9, choices=TERMO)


    class Meta:
        unique_together = ['re_funcionario', 'unidade']
    
    def __str__(self):
        return f'Funcionário : {self.re_funcionario} '

    def save(self, *args, **kwargs): 
        self.nome = self.nome.upper()
        print(f'{self.id} : {self.nome} Foi salvo com sucesso! \n')
        super(Funcionario, self).save(*args, **kwargs) 


def create_user(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create_user(username=str(instance.unidade.id) + str(instance.re_funcionario))
        user.set_password(instance.re_funcionario)
        grupo = Group.objects.get(id=3)
        user.groups.add(grupo)
        user.save()
        print(user.username, "Foi salvo com sucesso!")
        instance.usuario = user
        instance.save()
    

post_save.connect(create_user, sender=Funcionario)


def update_func(sender, instance, created, **kwargs):
    if not created:
        registro = RegistroAutorizacao.objects.create(funcionario=instance, acao=instance.termo_dados)
        registro.save()

post_save.connect(update_func, sender=Funcionario)
    

class RegistroAutorizacao(models.Model):
    funcionario = models.ForeignKey(Funcionario, related_name="logs", on_delete=models.PROTECT)
    data_atualizacao = models.DateTimeField(verbose_name='Atualização', auto_now_add=True)     
    acao = models.CharField(verbose_name="Ação", max_length=9, choices=TERMO, default=1)

    class Meta:
        verbose_name = 'Registro de Autorizações'
        verbose_name_plural = 'Registro de Autorizações'
