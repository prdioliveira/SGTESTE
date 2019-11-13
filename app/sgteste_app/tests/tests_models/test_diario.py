from django.test import TestCase
from app.sgteste_app.models.diario_models import Diario
from app.sgteste_app.models.projeto_models import Projeto
from django.core.management import call_command
from datetime import date


class DiarioTestCase(TestCase):
    def setUp(self):
        self.data = date.today().strftime('%Y-%m-%d')
        call_command('loaddata', 'initial_data.json', verbosity=0)

        self.projeto = Projeto.objects.create(
            nome_projeto="PRJ15002 - Projeto Teste",
            responsavel="John Doe",
            data_inicial=self.data,
            dias_execucao=15,
            quantidade_ct=150,
            status_projeto_id=1
        )

        self.diario = Diario.objects.create(
            data_execucao=self.data,
            cts_previstos=10,
            cts_executados=5,
            bugs_encontrados=0,
            cts_cancelados=1,
            observacao="Criação do Cenário de Teste",
            projeto_id=self.projeto.id

        )

    def test_diario_model(self):
        self.assertEqual(str(self.diario), self.diario.data_execucao)