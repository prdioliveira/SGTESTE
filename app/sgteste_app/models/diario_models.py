from django.db import models
from app.sgteste_app.models.projeto_models import Projeto


class Diario(models.Model):
    class Meta:
        db_table = 'diario'
        verbose_name = 'diario'
        verbose_name_plural = 'diarios'

    data_execucao = models.DateField()
    cts_previstos = models.IntegerField(null=True, blank=True)
    cts_executados = models.IntegerField(null=True, blank=True, default=0)
    bugs_encontrados = models.IntegerField(default=0, null=True, blank=True)
    cts_cancelados = models.IntegerField(default=0, null=True, blank=True)
    observacao = models.TextField(max_length=5000, null=True, blank=True, default='')
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)

    def __str__(self):
        return self.data_execucao