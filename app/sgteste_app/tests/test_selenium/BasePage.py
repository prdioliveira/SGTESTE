class BasePage(object):
    url = None

    def __init__(self, driver, live_server_url):
        self.driver = driver
        self.live_server_url = live_server_url

    def fill_form_by_id(self, element_id, value):
        elem = self.driver.find_element_by_id(element_id)
        elem.send_keys(value)

    def get_button_click(self, elemen_id):
        elemen = self.driver.find_element_by_id(elemen_id)
        elemen.click()

    def click_in_field(self, elemen_id):
        elemen = self.driver.find_element_by_id(elemen_id)
        elemen.click()

    @property
    def title(self):
        return self.driver.title

    def navigate(self):
        self.driver.get(
            "{}{}".format(
                self.live_server_url,
                self.url
            )
        )


class PesquisaPage(BasePage):
    url = "/sg-teste/"

    def set_nome_projeto(self, nome_projeto):
        self.fill_form_by_id("id_nome_projeto", nome_projeto)

    def set_responsavel(self, responsavel):
        self.fill_form_by_id("id_responsavel", responsavel)

    def page_cadastrar(self):
        self.get_button_click("btn-cadastrar")

    def btn_view_projeto(self):
        self.get_button_click("view_project")
        return ProfilePage(self.driver, self.live_server_url)


class CadastroPage(BasePage):
    url = "/cadastro-projeto/"

    def set_nome_porjeto(self, nome_projeto):
        self.fill_form_by_id("id_nome_projeto", nome_projeto)

    def set_data_inicio(self, data_inicial):
        self.fill_form_by_id("id_data_inicial", data_inicial)

    def set_dias_execucao(self, quantidade_dias):
        self.fill_form_by_id("id_dias_execucao", quantidade_dias)

    def click_field(self):
        self.click_in_field("id_dias_execucao")

    def set_casos_teste(self, quantidade_ct):
        self.fill_form_by_id("id_quantidade_ct", quantidade_ct)

    def set_responsavel(self, responsavel):
        self.fill_form_by_id("id_responsavel", responsavel)

    def getCadastroForm(self):
        return CadastroPage(self.driver, self.live_server_url)

    def submit(self):
        self.get_button_click("btn-save")
        return ProfilePage(self.driver, self.live_server_url)


class ProfilePage(BasePage):
    pass


class Homepage(BasePage):
    url = "/sg-teste/"

    def getCadastroForm(self):
        return CadastroPage(self.driver, self.live_server_url)

    def getPesquisaForm(self):
        return PesquisaPage(self.driver, self.live_server_url)
