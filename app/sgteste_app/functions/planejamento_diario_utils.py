from app.sgteste_app.functions.gerencia_functions import get_ct_restante
from app.sgteste_app.models.diario_models import Diario
import datetime
from math import ceil
from django.db.models import Sum

from app.sgteste_app.models.projeto_models import Projeto


def iterdates(date1, date2):
    one_day = datetime.timedelta(days=1)
    current = date1
    while current < date2:
        yield current
        current += one_day


def create_planning(initial_date, final_date, cts, project_id, number_of_days):
    one_day = datetime.timedelta(days=1)
    contador = 0
    x = 1
    last_date = ''
    for d in iterdates(initial_date, final_date):
        if d.weekday() not in (5, 6):
            # print(d, d.weekday(), calcula_planejamento(cts, qtd_dias))
            Diario.objects.create(data_execucao=d, cts_previstos=calculate_avg(cts, number_of_days), projeto_id=project_id)
        else:
            contador += 1
        last_date = d + one_day

    while x <= contador:
        if last_date.weekday() in (5, 6):
            last_date += one_day
            contador += 1
        else:
            Diario.objects.create(data_execucao=last_date, cts_previstos=calculate_avg(cts, number_of_days), projeto_id=project_id)
            last_date += one_day
        x += 1
    diff = diff_test_case_previstos(project_id)
    if diff > 0:
        fit_planning(project_id, cts, number_of_days)


# Retorna a quantidade de CTS por dia
def calculate_avg(cts, qtd_dias):
    media = ceil(cts/qtd_dias)
    return media


def get_next_id(model_class):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("select nextval('%s_id_seq')" % model_class._meta.db_table)
    row = cursor.fetchone()
    cursor.close()
    return row[0]


def sum_test_case(project_id):
    test_case = Diario.objects.filter(projeto_id=project_id).aggregate(cts_previstos=Sum('cts_previstos'))
    quantidade_cts = test_case['cts_previstos']

    return quantidade_cts


def get_test_case_in_prj(project_id):
    projeto = Projeto.objects.get(pk=project_id)
    quantidade_inicial = projeto.quantidade_ct

    return quantidade_inicial


def diff_test_case_previstos(project_id):
    test_case_diario = sum_test_case(project_id)
    test_case_projeto = get_test_case_in_prj(project_id)

    diff = test_case_diario - test_case_projeto

    return diff


def fit_planning(project_id, cts, number_of_days):
    diff = diff_test_case_previstos(project_id)
    cont = 0
    while cont < diff:
        id_diario = Diario.objects.filter(projeto_id=project_id).order_by('-data_execucao')[cont].id
        upd_new = calculate_avg(cts, number_of_days) - 1
        Diario.objects.filter(pk=id_diario).update(cts_previstos=upd_new)
        cont += 1


def add_planning(initial_date, final_date, cts, project_id, number_of_days):
    one_day = datetime.timedelta(days=1)
    contador = 0
    x = 1
    last_date = ''
    for d in iterdates(initial_date, final_date):
        if d.weekday() not in (5, 6):
            # print(d, d.weekday(), calcula_planejamento(cts, qtd_dias))
            Diario.objects.create(data_execucao=d, cts_previstos=calculate_avg(cts, number_of_days), projeto_id=project_id)
        else:
            contador += 1
        last_date = d + one_day

    while x <= contador:
        if last_date.weekday() in (5, 6):
            last_date += one_day
            contador += 1
        else:
            Diario.objects.create(data_execucao=last_date, cts_previstos=calculate_avg(cts, number_of_days), projeto_id=project_id)
            last_date += one_day
        x += 1


def update_pos_execute(project_id, diario_id, cts_executados):
    diario = Diario.objects.filter(projeto_id=project_id, cts_executados=0)
    cts_previstos_diario = get_cts_previstos_in_diario(diario_id)
    print('cts_previstos_diario', cts_previstos_diario)
    cts_executados_diario = get_ct_exec_in_diario(int(cts_executados))
    print('cts_executados_diario', cts_executados_diario)
    diff_exec_to_previsto = cts_executados_diario - cts_previstos_diario
    dias = len(diario)
    total_for_recalculate = 0
    if diff_exec_to_previsto > 0:
        total_for_recalculate = sum_test_case_previstos_for_update(project_id) - diff_exec_to_previsto
    else:
        total_for_recalculate = sum_test_case_previstos_for_update(project_id) + diff_exec_to_previsto

    media = calculate_avg(total_for_recalculate, dias)
    print('media', media)

    for d in diario:
        Diario.objects.filter(pk=d.id).update(cts_previstos=media)
        print(d.data_execucao)

    fit_planning_for_update(project_id, total_for_recalculate, len(diario))
    print('-----------', total_for_recalculate)


# soma a quantidade de casos de teste ainda não executados
def sum_test_case_previstos_for_update(project_id):
    cts_previstos = Diario.objects.filter(projeto_id=project_id,
                                          cts_executados=0).aggregate(
        cts_previstos=Sum('cts_previstos')
    )

    cts_executados = Diario.objects.filter(projeto_id=project_id,
                                           cts_executados=0).aggregate(
        cts_executados=Sum('cts_executados')
    )

    bugs_encontrados = Diario.objects.filter(projeto_id=project_id,
                                             cts_executados=0).aggregate(
        bugs_encontrados=Sum('bugs_encontrados')
    )

    total_cts = cts_previstos['cts_previstos'] - cts_executados['cts_executados'] - bugs_encontrados['bugs_encontrados']

    return total_cts


# retorna a quantidade de casos executados no dia
def get_ct_exec_in_diario(cts_executados):
    return cts_executados


# retorna a quantidade de casos previstos no dia
def get_cts_previstos_in_diario(diario_id):
    diario = Diario.objects.get(pk=diario_id)
    cts_previstos = diario.cts_previstos

    return cts_previstos


def fit_planning_for_update(project_id, cts, number_of_days):
    diff = diff_planejado_2_diff_sum_diario(project_id)
    cont = 0
    while cont < diff:
        id_diario = Diario.objects.filter(projeto_id=project_id, cts_executados=0).order_by('-data_execucao')[cont].id
        upd_new = calculate_avg(cts, number_of_days) - 1
        Diario.objects.filter(pk=id_diario).update(cts_previstos=upd_new)
        cont += 1
    alt = 0
    while cont > diff:
        id_diario = Diario.objects.filter(projeto_id=project_id, cts_executados=0).order_by('data_execucao')[alt].id
        upd_new = calculate_avg(cts, number_of_days) + 1
        Diario.objects.filter(pk=id_diario).update(cts_previstos=upd_new)
        cont -= 1
        alt += 1


def get_total_cts_executados(project_id):
    cts_executados = Diario.objects.filter(projeto_id=project_id,
                                           cts_executados__gt=0).aggregate(
        cts_executados=Sum('cts_executados')
    )
    executados = cts_executados['cts_executados']

    return executados


def diff_planejado_2_diff_sum_diario(project_id):
    sum_ct_restante = sum_test_case_previstos_for_update(project_id)
    total_ct_prj = Projeto.objects.get(pk=project_id).quantidade_ct
    total_cts_executados = get_total_cts_executados(project_id)
    cts = total_ct_prj - total_cts_executados

    total = sum_ct_restante - cts

    return total