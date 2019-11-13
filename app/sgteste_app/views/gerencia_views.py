from django.shortcuts import render
from django.db.models import Sum
from app.sgteste_app.models.diario_models import Diario
from app.sgteste_app.models.projeto_models import Projeto
from app.sgteste_app.functions.gerencia_functions import get_ct_restante
from app.sgteste_app.functions.gerencia_functions import get_dias_executados
from app.sgteste_app.functions.gerencia_functions import get_cts_adicionais
from app.sgteste_app.functions.gerencia_functions import get_dias_adicionais
from app.sgteste_app.functions.utils import paginattion_create


def acompanhamento_diario(request, projeto_id):
    projeto = Projeto.objects.get(pk=projeto_id)
    diario = Diario.objects.filter(projeto_id=projeto_id).order_by('data_execucao')
    diario_qtd_cts = Diario.objects.filter(projeto_id=projeto_id).aggregate(cts_executados=Sum('cts_executados'))

    cts_restantes = get_ct_restante(projeto_id)
    dias_executados = get_dias_executados(projeto_id)
    cts_adicionais = get_cts_adicionais(projeto)
    dias_adicionais = get_dias_adicionais(projeto)

    return render(
        request,
        'gerencia/acompanhamento-projeto-diario.html',
        {'projeto': projeto,
         'diario': diario,
         'diario_qtd_cts': diario_qtd_cts,
         'cts_restantes': cts_restantes,
         'dias_executados': dias_executados,
         'dias_adicionais': dias_adicionais,
         'cts_adicionais': cts_adicionais}
    )


def visualizar_acompanhamento_diario(request, projeto_id, pk):
    projeto = Projeto.objects.get(pk=projeto_id)
    diario = Diario.objects.get(pk=pk)

    return render(request, 'gerencia/visualizar-execucao-diario.html',
                  {'projeto': projeto, 'diario': diario})


def acompanhar_execucao(request):
    reg_per_page = 10
    all_projetos_list = Projeto.objects.order_by('-id')
    all_projetos = paginattion_create(all_projetos_list, reg_per_page, request)

    query_projeto = request.GET.get('nome_projeto')
    query_responsavel = request.GET.get('responsavel')

    if query_projeto is None:
        query_projeto = ''

    if query_responsavel is None:
        query_responsavel = ''

    if query_projeto and query_responsavel:
        all_projetos_list = all_projetos_list.filter(
            nome_projeto__icontains=query_projeto) | all_projetos_list.filter(
            responsavel__icontains=query_responsavel)
        all_projetos = paginattion_create(all_projetos_list, reg_per_page,
                                          request)
        return render(request, 'gerencia/acompanhar-execucao-projeto.html', {
            'projetos': all_projetos,
            'query_projeto': query_projeto,
            'query_responsavel': query_responsavel
        })

    if query_projeto or query_responsavel:
        if query_projeto:
            all_projetos_list = all_projetos_list.filter(
                nome_projeto__icontains=query_projeto)
            all_projetos = paginattion_create(all_projetos_list, reg_per_page,
                                              request)
            return render(request, 'gerencia/acompanhar-execucao-projeto.html', {
                'projetos': all_projetos,
                'query_projeto': query_projeto,
                'query_responsavel': query_responsavel
            })
        else:
            all_projetos_list = all_projetos_list.filter(
                responsavel__icontains=query_responsavel)
            all_projetos = paginattion_create(all_projetos_list, reg_per_page,
                                              request)
            return render(request, 'gerencia/acompanhar-execucao-projeto.html', {
                'projetos': all_projetos,
                'query_projeto': query_projeto,
                'query_responsavel': query_responsavel
            })

    return render(request, 'gerencia/acompanhar-execucao-projeto.html', {
        'projetos': all_projetos,
        'query_projeto': query_projeto,
        'query_responsavel': query_responsavel
    })