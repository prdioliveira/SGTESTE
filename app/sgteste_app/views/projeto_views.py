from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from app.sgteste_app.forms.projeto_forms import ProjetoForm
from app.sgteste_app.models.fixtures_models import StatusProjeto
from app.sgteste_app.models.projeto_models import Projeto
from app.sgteste_app.functions.utils import paginattion_create
from app.sgteste_app.functions.planejamento_diario_utils import create_planning


def cadastrar_projeto(request):
    if request.method == 'POST':
        form = ProjetoForm(request.POST)
        if form.is_valid():
            projeto = form.save(commit=False)
            status_oprojeto = StatusProjeto.objects.get(status='Planejado').id
            projeto.status_projeto_id = status_oprojeto
            projeto.save()

            # Criando o diario de teste
            data_inicial = datetime.strptime(
                str(projeto.data_inicial),
                '%Y-%m-%d').date()

            data_final = datetime.strptime(
                str(projeto.data_inicial),
                '%Y-%m-%d').date() + timedelta(days=projeto.dias_execucao)

            create_planning(
                initial_date=data_inicial,
                final_date=data_final,
                cts=projeto.quantidade_ct,
                project_id=projeto.id,
                number_of_days=projeto.dias_execucao
            )

            return redirect('sgteste_app:cadastrar_projeto')
    else:
        form = ProjetoForm()
        return render(request, 'projeto/cadastrar-projeto.html', {'form': form})


def pesquisar_projeto(request):
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
            nome_projeto__icontains=query_projeto)|all_projetos_list.filter(
            responsavel__icontains=query_responsavel)

        all_projetos = paginattion_create(
            all_projetos_list, reg_per_page, request)

        return render(request, 'projeto/pesquisar-projeto.html', {
            'projetos': all_projetos,
            'query_projeto': query_projeto,
            'query_responsavel': query_responsavel
        })

    if query_projeto or query_responsavel:
        if query_projeto:
            all_projetos_list = all_projetos_list.filter(
                nome_projeto__icontains=query_projeto)

            all_projetos = paginattion_create(
                all_projetos_list, reg_per_page, request)

            return render(request, 'projeto/pesquisar-projeto.html', {
                'projetos': all_projetos,
                'query_projeto': query_projeto,
                'query_responsavel': query_responsavel
            })
        else:
            all_projetos_list = all_projetos_list.filter(
                responsavel__icontains=query_responsavel)

            all_projetos = paginattion_create(
                all_projetos_list, reg_per_page, request)

            return render(request, 'projeto/pesquisar-projeto.html', {
                'projetos': all_projetos,
                'query_projeto': query_projeto,
                'query_responsavel': query_responsavel
            })

    return render(request, 'projeto/pesquisar-projeto.html', {
        'projetos': all_projetos,
        'query_projeto': query_projeto,
        'query_responsavel': query_responsavel,
    })


def editar_projeto(request, pk):
    projeto = get_object_or_404(Projeto, pk=pk)
    if request.method == 'POST':
        form = ProjetoForm(request.POST, instance=projeto)
        if form.is_valid():
            projeto = form.save(commit=False)
            if projeto.status_projeto_id == 1:
                projeto.save()
            else:
                return HttpResponseForbidden('<h1>Permissão Negada</h1><br>'
                                             '<a href="/pesquisar-projeto/">'
                                             'Voltar</a>')

            return redirect('sgteste_app:pesquisar_projeto')
    else:
        form = ProjetoForm(instance=projeto)
        return render(
            request,
            'projeto/editar-projeto.html',
            {
                'form': form,
                'projeto': projeto
            })


def excluir_projeto(request, pk):
    projeto = get_object_or_404(Projeto, pk=pk)
    if projeto.status_projeto_id == 1:
        projeto.delete()
        return redirect('sgteste_app:pesquisar_projeto')