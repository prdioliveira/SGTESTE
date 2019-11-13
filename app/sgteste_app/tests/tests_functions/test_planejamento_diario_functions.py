from django.test import TestCase
from app.sgteste_app.functions.planejamento_diario_utils import calculate_avg
from app.sgteste_app.functions.planejamento_diario_utils import create_planning
from app.sgteste_app.models.projeto_models import Projeto
from django.core.management import call_command
from datetime import date, timedelta, datetime
from app.sgteste_app.models.diario_models import Diario


class PlanejamentoDiarioFunctionsTestCase(TestCase):
    def setUp(self):
        call_command('loaddata', 'initial_data.json', verbosity=0)
        self.initial_date = date.today()
        self.datas = [15]
        self.projeto = Projeto.objects.create(
            nome_projeto="PRJ15002 - Projeto Teste",
            responsavel="John Doe",
            data_inicial=self.initial_date,
            dias_execucao=15,
            quantidade_ct=150,
            status_projeto_id=1
        )

        self.final_date = datetime.strptime(str(self.projeto.data_inicial), '%Y-%m-%d').date() +\
                          timedelta(days=self.projeto.dias_execucao)

    def test_calculate_avg(self):
        self.avg = calculate_avg(cts=self.projeto.quantidade_ct,
                                 qtd_dias=self.projeto.dias_execucao)
        self.assertEqual(self.avg, 10)

    def test_create_planning(self):
        create_planning(
            initial_date=self.initial_date,
            final_date=self.final_date,
            cts=self.projeto.quantidade_ct,
            project_id=self.projeto.id,
            number_of_days=self.projeto.dias_execucao
        )
        self.diario = Diario.objects.all()
        for d in self.diario:
            self.datas.append(d.data_execucao)
            self.assertEqual(self.projeto.id, d.projeto_id)
            self.assertIn(self.initial_date, self.datas)
