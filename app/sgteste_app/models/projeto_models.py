from django.db import models
from .fixtures_models import StatusProjeto


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
    gitlab_file = models.CharField(max_length=1500, null=True, blank=True)

    def __str__(self):
        return self.nome_projeto
