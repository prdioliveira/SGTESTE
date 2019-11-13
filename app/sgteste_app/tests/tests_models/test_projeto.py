from django.test import TestCase
from app.sgteste_app.models.projeto_models import Projeto
from django.core.management import call_command
from datetime import date


class ProjetoTesteCase(TestCase):
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

    def test_projeto_model(self):
        self.assertEqual(str(self.projeto), self.projeto.nome_projeto)