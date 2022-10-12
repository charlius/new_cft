import requests
from bs4 import BeautifulSoup


class notasProcess():

    def __init__(self, rut, password) -> None:
        self.data_form = {
            "_token": "",
            "rut": rut,
            "password": password
        }
        print("entro al processo")
        self.LOGIN_URL = "https://portal.cftsanagustin.cl/iniciar_sesion"
        self.URL = "https://portal.cftsanagustin.cl/concentracion_notas"
        self.client = requests.Session()
        soup = self.get_soup(self.LOGIN_URL)
        self.set_sessions(soup)


    def get_soup(self, url):
        html = self.client.get(url).content
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def set_sessions(self, soup):
        print(soup)
        _token = soup.find("input", {"name":"_token"})["value"]
        self.data_form["_token"] = _token
        self.client.post(self.LOGIN_URL, data=self.data_form)

    def get_data_head(self, table):
        thead = table.find("thead")
        td = thead.find_all("td")

        return [data.text for data in td]
    def get_data_body(self, table):
        data_body_list = []
        thead = table.find("tbody")
        tr_body = thead.find_all("tr")

        for tr in tr_body:
            td = tr.find_all("td")
            td_body = [data.text.replace("\t", "").replace("\n","") for data in td]

            data_body_list.append(td_body)
        return data_body_list

    def set_head_with_body_data(self, data_body_list, data_head):
        notas_list = []
        for data in data_body_list:

            cont = 0
            notas = {}
            for dh in data_head:
                notas[dh] = data[cont].strip()
                cont = cont + 1
            notas_list.append(notas)
        return notas_list

    def get_notas(self, soup, periodo):

        # Buscar tabla por semestre
        div_table = soup.find('div', {"id": f"n2022-{periodo}"})
        table =  div_table.find('table')

        # Obtener el encabezado de la tabla
        data_head = self.get_data_head(table)
        # Obtener la data del body
        data_body_list = self.get_data_body(table)

        return self.set_head_with_body_data(data_body_list, data_head)

    def get_nombre(self, soup):
        a = soup.find("a", {"id": "userDropdown"})
        nombre_spam = a.find("span").text.replace("\t", "").replace("\n","").strip()
        nombre_list = nombre_spam.replace(" ", ",").split(",")

        nombre = ""
        for n in nombre_list:
            if n:
                nombre = f"{nombre} {n}"

        return nombre.strip()

    def get_data(self, periodo):
        soup = self.get_soup(self.URL)
        notas = self.get_notas(soup, periodo)
        nombre = self.get_nombre(soup)

        return {
            "notas": notas,
            "nombre": nombre
        }