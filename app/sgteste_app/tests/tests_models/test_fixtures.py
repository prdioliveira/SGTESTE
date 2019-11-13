from django.test import TestCase
from django.core.management import call_command
from app.sgteste_app.models.fixtures_models import StatusProjeto


class FixturesTestCase(TestCase):
    def setUp(self):
        call_command('loaddata', 'initial_data.json', verbosity=0)

    def test_fixtures_model(self):
        status = ['Planejado', 'Em execução', 'Concluído']

        for st in status:
            self.assertIn(st, str(StatusProjeto.objects.all()))