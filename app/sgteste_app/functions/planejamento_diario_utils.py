from psycopg2._psycopg import DatabaseError

from app.sgteste_app.models.diario_models import Diario
import datetime
from math import ceil
from django.db.models import Sum
from app.sgteste_app.models.projeto_models import Projeto


def iterdates(date1, date2):
    """
    :param date1: data inicial
    :param date2: data final
    :return: uma lista de data contendo apenas os dias uteis, exeto feriados
    """
    one_day = datetime.timedelta(days=1)
    current = date1
    while current < date2:
        yield current
        current += one_day


def create_planning(initial_date, final_date, cts, project_id, number_of_days):
    """

    :param initial_date: data inicial
    :param final_date: data final
    :param cts: quantidade de casos de teste do projeto
    :param project_id: id do projeto
    :param number_of_days: quantidade de dias para a execução
    :return: realiza a atualização no banco inserindo a quantidade de CTS p/dia
    """
    one_day = datetime.timedelta(days=1)
    contador = 0
    x = 1
    last_date = ''
    for d in iterdates(initial_date, final_date):
        if d.weekday() not in (5, 6):
            # print(d, d.weekday(), calcula_planejamento(cts, qtd_dias))
            try:
                Diario.objects.create(data_execucao=d, cts_previstos=calculate_avg(cts, number_of_days), projeto_id=project_id)
            except DatabaseError as error:
                print(error)
        else:
            contador += 1
        last_date = d + one_day

    while x <= contador:
        if last_date.weekday() in (5, 6):
            last_date += one_day
            contador += 1
        else:
            try:
                Diario.objects.create(data_execucao=last_date, cts_previstos=calculate_avg(cts, number_of_days), projeto_id=project_id)
            except DatabaseError as error:
                print(error)
            last_date += one_day
        x += 1
    diff = diff_test_case_previstos(project_id)
    if diff > 0:
        fit_planning(project_id, cts, number_of_days)


# Retorna a quantidade de CTS por dia
def calculate_avg(cts, qtd_dias):
    """

    :param cts: quantidade de casos de teste
    :param qtd_dias: quantidade de dias para execução
    :return: a media de casos de teste por dia arredondado para cima
    """
    media = ceil(cts/qtd_dias)
    return media


def get_next_id(model_class):
    """

    :param model_class: Model Class
    :return: returna o proximo id do model
    """
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("select nextval('%s_id_seq')" % model_class._meta.db_table)
    row = cursor.fetchone()
    cursor.close()
    return row[0]


def sum_test_case(project_id):
    """

    :param project_id: id do projeto
    :return: quantidade de casos de teste do projeto conforme id
    """
    quantidade_cts = 0
    try:
        test_case = Diario.objects.filter(projeto_id=project_id).aggregate(cts_previstos=Sum('cts_previstos'))
        quantidade_cts = test_case['cts_previstos']
    except DatabaseError as error:
        print(error)

    return quantidade_cts


def get_test_case_in_prj(project_id):
    """

    :param project_id: id do projeto
    :return: quantidade inicial de casos de teste planejados
    """
    projeto = Projeto.objects.get(pk=project_id)
    quantidade_inicial = projeto.quantidade_ct

    return quantidade_inicial


def diff_test_case_previstos(project_id):
    """

    :param project_id: id do projeto
    :return: diferença entre o total inserido, conforme media e o total inicial
    planejado
    """
    test_case_diario = sum_test_case(project_id)
    test_case_projeto = get_test_case_in_prj(project_id)

    diff = test_case_diario - test_case_projeto

    return diff


def fit_planning(project_id, cts, number_of_days):
    """

    :param project_id: id do projeto
    :param cts: quantidade de casos de teste planejados inicialmente
    :param number_of_days: quantidade de dias para execução
    :return: ajusta no db a quantidade de casos de teste. A soma da media dos
    casos de teste inseridos no diario é maior que o planejado inicialmente.
    Em ordem decrescente por data, vai reduzindo um CT até atingir o valor
    planejado inicialmente.
    """
    diff = diff_test_case_previstos(project_id)
    cont = 0
    while cont < diff:
        try:
            id_diario = Diario.objects.filter(projeto_id=project_id).order_by('-data_execucao')[cont].id
            upd_new = calculate_avg(cts, number_of_days) - 1
            Diario.objects.filter(pk=id_diario).update(cts_previstos=upd_new)
        except DatabaseError as error:
            print(error)
        cont += 1


def add_planning(initial_date, final_date, cts, project_id, number_of_days):
    """

    :param initial_date: data inicial
    :param final_date: data final
    :param cts: quantidade de casos de teste
    :param project_id: id do projeto
    :param number_of_days: numero de dias para execução
    :return: insere no db, na proxima data util a quantidade de CTS planejdos.
    Insere casos de teste adicionais, ou seja, mais um dia para a execução.
    """
    one_day = datetime.timedelta(days=1)
    contador = 0
    x = 1
    last_date = ''
    try:
        cts_adicionais = Projeto.objects.get(pk=project_id).cts_adicionais
        cts_adicionais += int(cts)
        Projeto.objects.filter(pk=project_id).update(cts_adicionais=cts_adicionais)
    except DatabaseError as error:
        print(error)
    for d in iterdates(initial_date, final_date):
        if d.weekday() not in (5, 6):
            # print(d, d.weekday(), calcula_planejamento(cts, qtd_dias))
            try:
                Diario.objects.create(data_execucao=d, cts_previstos=calculate_avg(cts, number_of_days), projeto_id=project_id)
            except DatabaseError as error:
                print(error)
        else:
            contador += 1
        last_date = d + one_day

    while x <= contador:
        if last_date.weekday() in (5, 6):
            last_date += one_day
            contador += 1
        else:
            try:
                Diario.objects.create(data_execucao=last_date, cts_previstos=calculate_avg(cts, number_of_days), projeto_id=project_id)
                last_date += one_day
            except DatabaseError as error:
                print(error)
        x += 1


def update_pos_execute(project_id, diario_id, cts_executados):
    """

    :param project_id: id do projeto
    :param diario_id: id do diario da execução
    :param cts_executados: quantidade de cts executados (retornado da tela no
    momento da inserção)
    :return: Ajusta a media dos casos de teste após a execução do teste.
    """
    diario = Diario.objects.filter(projeto_id=project_id, cts_executados=0)
    cts_previstos_diario = get_cts_previstos_in_diario(diario_id)
    cts_executados_diario = get_ct_exec_in_diario(int(cts_executados))
    diff_exec_to_previsto = cts_executados_diario - cts_previstos_diario
    dias = len(diario)
    total_for_recalculate = 0
    if dias > 0 and dias is not None:
        pass
    else:
        diff_exec_to_previsto = diff_exec_to_previsto * -1
        data = Diario.objects.filter(projeto_id=project_id).order_by('-data_execucao')[0].data_execucao
        initial_date = data + datetime.timedelta(days=1)
        final_date = data + datetime.timedelta(days=2)
        add_planning(initial_date, final_date, 0, project_id, 1)


def sum_test_case_previstos_for_update(project_id):
    """

    :param project_id: id projeto
    :return: soma dos casos de teste ainda não executados
    """
    total_cts = 0
    try:
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
    except DatabaseError as error:
        print(error)

    return total_cts


def get_ct_exec_in_diario(cts_executados):
    """

    :param cts_executados: Quantidade de cts executados no dia (valor informado
    no campo da tela)
    :return: quantidade de cts executados no dia
    """
    return cts_executados


def get_cts_previstos_in_diario(diario_id):
    """

    :param diario_id: id do diario
    :return: quantidade de cts previstos para a execução no dia
    """
    cts_previstos = 0
    try:
        diario = Diario.objects.get(pk=diario_id)
        cts_previstos = diario.cts_previstos
    except DatabaseError as error:
        print(error)
    return cts_previstos


def fit_planning_for_update(project_id, cts, number_of_days):
    """

    :param project_id: id do projeto
    :param cts: quantidade de casos de testes
    :param number_of_days: quantidade de dias para a execução
    :return: Ajusta no db em ordem decrescente:
        se quantidade de cts executados for maior que a quantidade planejada,
        retira um CT até ajustar à quantidade planejada.
        se a quantidade de cts executados for menor que a quantidade planejada,
        adiciona um ct em orde crescente por data.
    """
    diff = diff_planejado_2_diff_sum_diario(project_id)
    cont = 0
    alt = 0
    count_id = 0
    if cont < diff:
        while cont < diff:
            try:
                id_diario = Diario.objects.filter(projeto_id=project_id, cts_executados=0).order_by('-data_execucao')[cont].id
                upd_new = calculate_avg(cts, number_of_days) - 1
                Diario.objects.filter(pk=id_diario).update(cts_previstos=upd_new)
            except DatabaseError as error:
                print(error)
            cont += 1
    else:
        cts_previstos = sum_test_case_previstos_for_update(project_id)
        diff_in_diff = diff + cts_previstos
        cont = 0
        alt = 0
        while cont > diff:
            id_diario = Diario.objects.filter(projeto_id=project_id, cts_executados=0).order_by('-data_execucao')[alt].id
            media = calculate_avg(cts_previstos + diff_in_diff, number_of_days) + 1
            # if media % 2 == 0:
            #     media = calculate_avg(cts_previstos, number_of_days) + 2
            Diario.objects.filter(pk=id_diario).update(cts_previstos=media)
            if alt == number_of_days - 1:
                alt = 0
            cont -= 1
            alt += 1




def get_total_cts_executados(project_id):
    """

    :param project_id: id do projeto
    :return: quantidade de cts executados
    """
    executados = 0
    try:
        cts_executados = Diario.objects.filter(projeto_id=project_id,
                                               cts_executados__gt=0).aggregate(
            cts_executados=Sum('cts_executados')
        )
        executados = cts_executados['cts_executados']
    except DatabaseError as error:
        print(error)

    return executados


def diff_planejado_2_diff_sum_diario(project_id):
    """

    :param project_id: id do projeto
    :return: a diferença entre o previsto e o planejado para saber quantos cts
    devem ser removidos ou inseridos, para utilização em fit_planning_for_update
    """
    sum_ct_restante = sum_test_case_previstos_for_update(project_id)
    total_ct_prj = Projeto.objects.get(pk=project_id).quantidade_ct + Projeto.objects.get(pk=project_id).cts_adicionais
    total_cts_executados = get_total_cts_executados(project_id)
    cts = total_ct_prj - total_cts_executados

    total = sum_ct_restante - cts

    return total