from app.sgteste_app.models.diario_models import Diario
from django.db.models import Sum, Count

from app.sgteste_app.models.projeto_models import Projeto


def get_ct_restante(projeto_id):
    """

    :param projeto_id: id do projeto
    :return: quantidade de cts que ainda restam executar
    """
    qtd_cts_previstos = Projeto.objects.get(pk=projeto_id).quantidade_ct
    diario_qtd_cts = Diario.objects.filter(projeto_id=projeto_id).aggregate(
        cts_executados=Sum('cts_executados'),
        cts_cancelados=Sum('cts_cancelados')
    )

    cts_restantes = qtd_cts_previstos - diario_qtd_cts['cts_executados'] - \
                    diario_qtd_cts['cts_cancelados']

    return cts_restantes


def get_dias_executados(projeto_id):
    """

    :param projeto_id: id do projeto
    :return: quantidade de dias em que houve execução
    """
    executados = Diario.objects.filter(
        projeto_id=projeto_id, cts_executados__gt=0).aggregate(
        dias_exec=Count('cts_executados'))

    dias_executados = executados['dias_exec']

    return dias_executados


def get_cts_adicionais(object):
    cts_adicionais = object.cts_adicionais
    return cts_adicionais


def get_dias_adicionais(object):
    add = Diario.objects.filter(
        projeto_id=object.id).aggregate(total_dias=Count('data_execucao'))

    adicionais = add['total_dias']
    dias_adicionais = adicionais - object.dias_execucao

    return dias_adicionais