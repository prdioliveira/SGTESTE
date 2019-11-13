from app.sgteste_app.models.projeto_models import Projeto


def update_quantidade_cts(project_id, cts):
    Projeto.objects.filter(pk=project_id).update(quantidade_ct=cts)


def get_quantidade_cts(projecc_id):
    quantidade_cts = Projeto.objects.get(pk=projecc_id).quantidade_ct

    return quantidade_cts
