from django.conf.urls import url
from app.sgteste_app.views import projeto_views, diario_views, gerencia_views, \
    relatorio_views

app_name = 'sgteste_app'

urlpatterns = [
    #Projeto
    url(r'^cadastro-projeto/$', projeto_views.cadastrar_projeto, name='cadastrar_projeto'),
    url(r'^pesquisar-projeto/$', projeto_views.pesquisar_projeto, name='pesquisar_projeto'),
    url(r'^cadastro-projeto/(?P<pk>[0-9]+)/editar/$', projeto_views.editar_projeto, name='editar_projeto'),
    url(r'^cadastro-projeto/(?P<pk>[0-9]+)/delete/$', projeto_views.excluir_projeto, name='deletar_projeto'),

    #Diario
    url(r'^diario-execucao/(?P<projeto_id>[0-9]+)/$', diario_views.lista_execucao, name='lista_execucao'),
    url(r'^diario-execucao/projeto/(?P<projeto_id>[0-9]+)/diario/(?P<pk>[0-9]+)/$', diario_views.executar_teste, name='executar_teste'),
    url(r'^diario-execucao/adicionar/(?P<projeto_id>[0-9]+)/$', diario_views.adicionar_planejamento, name='adicionar_planejamento'),

    # Gerencia
    url(r'^acompanhamento-diario/projeto/(?P<projeto_id>[0-9]+)/$', gerencia_views.acompanhamento_diario, name='acompanhamento_diario'),
    url(r'^view-acompanhamento-diario/projeto/(?P<projeto_id>[0-9]+)/diario/(?P<pk>[0-9]+)/$', gerencia_views.visualizar_acompanhamento_diario, name='visualizar_acompanhamento_diario'),
    url(r'^view-acompanhamento-execucao/$', gerencia_views.acompanhar_execucao, name='acompanhar_execucao'),

    #Relatorio
    url(r'^gerar-relatorio/$', relatorio_views.some_view, name='gerar_relatorio'),
]