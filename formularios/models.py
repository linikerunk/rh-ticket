from django.db import models
from datetime import datetime
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from chamados.models import Ticket, Categoria, SubCategoria
from perfil.models import Funcionario



AUSENCIA = (
    ("Falta", "Falta"),
    ("Atraso", "Atraso"),
    ("Saída Antecipada", "Saida Antecipada"),
    ("Saída Intermediária", "Saída Intermediária"),
)

JUSTIFICATIVA_AUSENCIA = (
    ('Débido em Banco de HS', 'Débido em Banco de HS'),
    ('Descanso de Jornadas', 'Descanso de Jornadas'),
    ('Serviço Externo', 'Serviço Externo'),
    ('Viagem à Trabalho', 'Viagem à Trabalho'),
    ('Treinamento Externo', 'Treinamento Externo'),
    ('Folga TRE', 'Folga TRE'),
)

class JustificativaAusencia(models.Model):
    data_inicio = models.DateTimeField(verbose_name="Data de Início")
    data_fim = models.DateTimeField(verbose_name="Data de Fim")
    tipo_de_ausencia = models.CharField(verbose_name="Tipo de Ausência", choices=AUSENCIA, max_length=19)
    justificativa = models.CharField(verbose_name="Justificativa", choices=JUSTIFICATIVA_AUSENCIA, max_length=21)
    observacao = models.TextField(verbose_name="Observação", max_length=250, blank=True)
    ticket = models.OneToOneField(Ticket, related_name="justificativa_ausencia", blank=True, null=True, verbose_name="Ticket", on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, related_name="justificativa_ausencia", on_delete=models.PROTECT)


    class Meta:
        verbose_name = 'Justificativa de Ausência'
        verbose_name_plural = 'Justificativas de Ausências'

    def __str__(self):
        return f'Justificativa de Ausencia número : {self.id}'


def create_ticket(sender, instance, created, **kwargs):
    if created:
        categoria = Categoria.objects.get(nome="Acesso")
        subcategoria = SubCategoria.objects.get(nome="Justificativa de Ausência")
        ticket = Ticket.objects.create(
            texto = f"\t[Data Início]: {instance.data_inicio.strftime('%d/%m/%Y')}  à  [Data Fim]: {instance.data_fim.strftime('%d/%m/%Y')}\n \
\t[Tipo de Justificativa de Ausência] : {instance.tipo_de_ausencia}, \n \
\t[Justificativa] : {instance.justificativa}, \n \
\t[Observação] : {instance.observacao}\n",
            funcionario =instance.funcionario,
            data=datetime.now(),
            categoria=categoria,
            subcategoria=subcategoria)
        ticket.save()
        instance.ticket = ticket
        instance.save()

post_save.connect(create_ticket, sender=JustificativaAusencia)