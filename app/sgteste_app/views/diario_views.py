from datetime import datetime as dt
import datetime
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from app.sgteste_app.forms.diario_forms import DiarioForm, AddInDiarioForm
from app.sgteste_app.functions.gerencia_functions import get_cts_adicionais, \
    get_dias_adicionais, get_ct_restante
from app.sgteste_app.models.diario_models import Diario
from app.sgteste_app.models.projeto_models import Projeto
from app.sgteste_app.functions.planejamento_diario_utils import add_planning, \
    update_pos_execute


def lista_execucao(request, projeto_id):
    if request.method == 'POST':
        if get_ct_restante(projeto_id) == 0:
            concluir_projeto(Projeto, projeto_id)
            return redirect('sgteste_app:pesquisar_projeto')
        else:
            tag_inicial = '<h2>'
            tag_final = '</h2>'
            msg1 = 'Permissão Negada. Não é possivel ' \
                   'concluir projeto com ct pendente'

            tag_br = '<br>'

            tag_a = '<a href="/diario-execucao/' + str(projeto_id) + '"' \
                    + '>Voltar</a>'

            return HttpResponseForbidden(tag_inicial + msg1 + tag_final +
                                         tag_br + tag_a)
    else:
        diario = Diario.objects.filter(projeto_id=projeto_id).order_by(
            'data_execucao')

        projeto = Projeto.objects.get(pk=projeto_id).nome_projeto
        prj = Projeto.objects.get(pk=projeto_id)
        diferenca_cts = get_cts_adicionais(prj)
        dias_adicionais = get_dias_adicionais(prj)
        cts_pendentes = get_ct_restante(projeto_id)
        return render(
            request,
            'diario/lista-execucao.html',
            {
                'diario': diario,
                'projeto_id': projeto_id,
                'projeto': projeto,
                'diferenca_cts': diferenca_cts,
                'dias_adicionais': dias_adicionais,
                'prj': prj,
                'cts_pendentes': cts_pendentes})


def executar_teste(request, pk, projeto_id):
    diario = get_object_or_404(Diario, pk=pk, projeto_id=projeto_id)
    if request.method == 'POST':
        executados = request.POST.get('cts_executados')
        cts_cancelados = request.POST.get('cts_cancelados')
        form = DiarioForm(request.POST, instance=diario)
        if form.is_valid():
            fdiario = form.save(commit=False)
            if executados != '0':
                status_prj = Projeto.objects.get(
                    pk=projeto_id).status_projeto_id

                if status_prj != 2:
                    Projeto.objects.filter(pk=projeto_id).update(
                        status_projeto_id=2)

                    fdiario.save()
                    update_pos_execute(
                        project_id=projeto_id,
                        diario_id=pk,
                        cts_executados=executados,
                        cts_cancelados=cts_cancelados)

                else:
                    fdiario.save()
                    update_pos_execute(
                        project_id=projeto_id,
                        diario_id=pk,
                        cts_executados=executados,
                        cts_cancelados=cts_cancelados)

            else:
                fdiario.save()
                update_pos_execute(
                    project_id=projeto_id,
                    diario_id=pk,
                    cts_executados=executados,
                    cts_cancelados=cts_cancelados)

            return redirect('sgteste_app:lista_execucao', projeto_id)
    else:
        form = DiarioForm(instance=diario)
        return render(
            request,
            'diario/executar-teste.html',
            {
                'form': form,
                'diario': diario})


def adicionar_planejamento(request, projeto_id):
    projeto = Projeto.objects.get(pk=projeto_id).id
    data = Diario.objects.filter(projeto_id=projeto).order_by(
        '-data_execucao')[0].data_execucao

    cts_previstos = request.POST.get('cts_previstos')
    if request.method == 'POST':
        add_planning(
            initial_date=data + datetime.timedelta(days=1),
            final_date=data + datetime.timedelta(days=2),
            cts=int(cts_previstos),
            project_id=projeto,
            number_of_days=1
        )
        return redirect('sgteste_app:lista_execucao', projeto_id)
    form = AddInDiarioForm()
    return render(
        request,
        'diario/adicionar-execucao.html',
        {
            'form': form,
            'projeto': projeto
        })


def concluir_projeto(Object, object_id):
    data_exec = Diario.objects.filter(projeto_id=object_id).order_by(
        '-data_execucao')[0].data_execucao

    Object.objects.filter(pk=object_id).update(
        data_conclusao=dt.strftime(data_exec, '%Y-%m-%d'))

    Object.objects.filter(pk=object_id).update(status_projeto_id=3)
