from django.core.management import call_command
from app.sgteste_app.tests.test_selenium.BasePage import Homepage
from app.sgteste_app.tests.test_selenium.base import FunctionalTest


class CadastroProjeto(FunctionalTest):

    def setUp(self):
        call_command('loaddata', 'initial_data.json', verbosity=0)

    def test_cadastro_page(self):
        nome_projeto = "PRJ0000-PROJETO PILOTO"
        homepage = Homepage(self.browser, self.live_server_url)
        homepage.navigate()
        cadastro_page = homepage.getCadastroForm()
        cadastro_page.navigate()
        cadastro_page.set_nome_porjeto(nome_projeto)
        cadastro_page.set_data_inicio("01/11/2019")
        cadastro_page.click_field()
        cadastro_page.set_dias_execucao("15")
        cadastro_page.set_casos_teste("107")
        cadastro_page.set_responsavel("Paulo")
        profile_page = cadastro_page.submit()
        self.assertEqual("Cadastro | Projeto", profile_page.title)
        message = self.browser.find_element_by_xpath("//div[1]/div/div/div").text
        self.assertIn(nome_projeto, message)

    def test_validar_cadastro(self):
        nome_projeto = "PRJ0000-PROJETO PILOTO"
        homepage = Homepage(self.browser, self.live_server_url)
        homepage.navigate()
        cadastro_page = homepage.getCadastroForm()
        cadastro_page.navigate()
        cadastro_page.set_nome_porjeto(nome_projeto)
        cadastro_page.set_data_inicio("01/11/2019")
        cadastro_page.click_field()
        cadastro_page.set_dias_execucao("15")
        cadastro_page.set_casos_teste("107")
        cadastro_page.set_responsavel("Paulo")
        profile_page = cadastro_page.submit()
        self.assertEqual("Cadastro | Projeto", profile_page.title)
        message = self.browser.find_element_by_xpath(
            "//div[1]/div/div/div").text

        self.assertIn(nome_projeto, message)
        homepage.navigate()
        pesquisa_page = homepage.getPesquisaForm()
        pesquisa_page.navigate()
        profile_page = pesquisa_page.btn_view_projeto()
        projeto = self.browser.find_element_by_xpath("//div/div/div[2]/div[1]/div/p").text
        self.assertEqual("Visualizar | Projeto", profile_page.title)
        self.assertIn(nome_projeto, projeto)
