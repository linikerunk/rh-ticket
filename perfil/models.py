from django.db import models
from auditlog.registry import auditlog
from datetime import datetime
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from auditlog.models import LogEntry 
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver # receiver PostSignal 2
from django.core.files.storage import default_storage
from django.conf import settings


PHOTOS_FOLDER = 'espelhos'
DEFAULT = '0000.JPG'
TERMO = (("Alteração", "Alteração"), ("Exclusão", "Exclusão"),)


class CustomLogEntry(LogEntry):
    
    class Meta:
        proxy = True


class Menu(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome


class Unidade(models.Model):
    nome = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=250, verbose_name="E-mail",
                              blank=True, default="")
    menu = models.ManyToManyField("Menu")
    grupo = models.ManyToManyField(Group)

    def __str__(self):
        return self.nome


class CentroDeCusto(models.Model):
    numero = models.CharField(max_length=12, verbose_name="Número Centro de Custo", unique=True)
    nome = models.CharField(max_length=100, blank=False, verbose_name="Nome do Centro de Custo")
    responsaveis = models.CharField(max_length=250, blank=True, null=True, verbose_name="Responsavei CharFields")

    def split_tags(self):
        return self.tags.split(',')

    def __str__(self):
        return f'CDC : {self.numero} Nome : {self.nome}'


class Funcionario(models.Model):
    re_funcionario = models.CharField(max_length=9, verbose_name="RE")
    nome = models.CharField(max_length=55, verbose_name="Funcionário :")
    admissao = models.CharField(max_length=20, blank=True, verbose_name="Data de Admissão : ", default="")
    demissao = models.CharField(max_length=20, blank=True, verbose_name="Data de Demissão : ", default="")
    ramal = models.CharField(max_length=9, blank=True, verbose_name="Ramal", default="")
    telefone = models.CharField(max_length=15, blank=True, verbose_name="Telefone", default="")
    email_corporativo = models.EmailField(max_length=254, verbose_name="Email Corporativo", blank=True, default="")
    email = models.EmailField(max_length=254, verbose_name="Email Pessoal", blank=True, default="")
    primeiro_acesso = models.BooleanField(verbose_name="Primeiro Acesso", default=True)
    termo_dados = models.CharField(verbose_name="Termo de Consentimento", max_length=9, blank=True, choices=TERMO)
    unidade = models.ForeignKey(Unidade, related_name="funcionarios", on_delete=models.PROTECT)
    # centro_de_custo = models.CharField(max_length=12, verbose_name="Centro de Custo")
    centro_de_custo_link = models.ForeignKey(CentroDeCusto, verbose_name="Centro de Custo link", null=True, on_delete=models.PROTECT)
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    espelho = models.ImageField(max_length=200, upload_to="espelhos",  default="0000.JPG", verbose_name='Fotos Funcionários')
    
    def get_photo_url(self):
        path = f'{PHOTOS_FOLDER}/{self.usuario}.JPG'

        if default_storage.exists(path): # Default of get url\
            return default_storage.url(path)
        
        print(f'{PHOTOS_FOLDER}/{DEFAULT}')
        return default_storage.url(f'{PHOTOS_FOLDER}/{DEFAULT}')

    class Meta:
        unique_together = ['re_funcionario', 'unidade']
    

    def __str__(self):
        return f'Funcionário : {self.re_funcionario} '


    def save(self, *args, **kwargs): 
        self.nome = self.nome.upper()
        print(f'{self.id} : {self.nome} Foi salvo com sucesso! \n')
        super(Funcionario, self).save(*args, **kwargs) 


auditlog.register(Funcionario, exclude_fields=['user'],  mapping_fields={'telefone': 'Telefone', 'email': 'E-mail Pessoal'})


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


class Item(models.Model):
    nome = models.CharField(max_length=150, verbose_name="Nome")

    def __str__(self):
        return self.nome


class Acesso(models.Model):
    item = models.ForeignKey(Item, "Item")
    grupo = models.ManyToManyField(Group, "Grupo")
    unidade = models.ManyToManyField(Unidade, "Unidade")

    def __str__(self):
        return f"Id :{self.id} Item :{self.item}"