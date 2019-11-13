from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from django.core.management import call_command


class CadastroProjetoSeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        call_command('loaddata', 'initial_data.json', verbosity=0)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_cadastro_projeto(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/cadastro-projeto/'))
        self.page_title = self.selenium.title
        self.assertEqual(self.page_title, "Cadastro | Projeto")
        input_nome_projeto = self.selenium.find_element_by_name("nome_projeto")
        input_data_inicial = self.selenium.find_element_by_name("data_inicial")
        input_dias_execucao = self.selenium.find_element_by_name("dias_execucao")
        input_qtd_ct = self.selenium.find_element_by_name("quantidade_ct")
        input_responsavel = self.selenium.find_element_by_name("responsavel")
        btn_save = self.selenium.find_element_by_id("btn-save")
        input_nome_projeto.send_keys("PRJ15000 - PROJETO TESTE")
        input_data_inicial.send_keys("01/11/2019")
        input_dias_execucao.click()
        input_dias_execucao.send_keys("15")
        input_qtd_ct.send_keys("150")
        input_responsavel.send_keys("Paulo Ricardo de Oliveira")
        btn_save.click()
