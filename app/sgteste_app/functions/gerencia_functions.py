from app.sgteste_app.models.diario_models import Diario
from django.db.models import Sum, Count


def get_ct_restante(projeto_id):
    diario_qtd_cts = Diario.objects.filter(
        projeto_id=projeto_id).aggregate(cts_previstos=Sum('cts_previstos'),
                                         cts_executados=Sum('cts_executados'),
                                         cts_cancelados=Sum('cts_cancelados'))

    cts_restantes = diario_qtd_cts['cts_previstos'] - \
                    diario_qtd_cts['cts_executados'] - \
                    diario_qtd_cts['cts_cancelados']

    return cts_restantes


def get_dias_executados(projeto_id):
    executados = Diario.objects.filter(
        projeto_id=projeto_id, cts_executados__gt=0).aggregate(
        dias_exec=Count('cts_executados'))

    dias_executados = executados['dias_exec']

    return dias_executados


def get_cts_adicionais(object):
    diario_qtd_cts = Diario.objects.filter(
        projeto_id=object.id).aggregate(cts_previstos=Sum('cts_previstos'),
                                        cts_executados=Sum('cts_executados'))

    cts_adicionais = diario_qtd_cts['cts_previstos'] - object.quantidade_ct

    return cts_adicionais


def get_dias_adicionais(object):
    add = Diario.objects.filter(
        projeto_id=object.id).aggregate(total_dias=Count('data_execucao'))

    adicionais = add['total_dias']
    dias_adicionais = adicionais - object.dias_execucao

    return dias_adicionais