from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from .fixtures_models import StatusProjeto
from app.sgteste_app.functions.utils import send_email


class Projeto(models.Model):
    class Meta:
        db_table = 'projeto'
        verbose_name = 'projeto'

    nome_projeto = models.CharField(max_length=100)
    responsavel = models.CharField(max_length=80)
    data_inicial = models.DateField()
    dias_execucao = models.IntegerField()
    quantidade_ct = models.IntegerField()
    status_projeto = models.ForeignKey(StatusProjeto, on_delete=models.PROTECT)
    data_conclusao = models.DateField(null=True, blank=True)
    cts_adicionais = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.nome_projeto
