import json
from operator import mod
import requests
from bs4 import BeautifulSoup


class horarioProcess():

    def __init__(self, rut, password) -> None:
        self.data_form = {
            "_token": "",
            "rut": rut,
            "password": password
        }
        print("entro al processo")
        self.LOGIN_URL = "https://portal.cftsanagustin.cl/iniciar_sesion"
        self.URL = "https://portal.cftsanagustin.cl/horario"
        self.client = requests.Session()
        soup = self.get_soup(self.LOGIN_URL)
        self.set_sessions(soup)



    def get_soup(self, url):
        html = self.client.get(url).content
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def set_sessions(self, soup):
        _token = soup.find("input", {"name":"_token"})["value"]
        self.data_form["_token"] = _token
        self.client.post(self.LOGIN_URL, data=self.data_form)

    def get_horario(self, soup):

        # obtener los datos del body, guardandolos en una lista
        table = soup.find("table", "table table-sm table-bordered")
        thead = table.find("tbody")

        tr_body = thead.find_all("tr")

        modulo_hora = []

        for tr in tr_body:
            td_data = {}
            td = tr.find_all("td")
            td_data["modulo"] = td[0].text
            td_data["hora"] = td[1].text
            modulo_hora.append(td_data)

        script = soup.find_all("script")
        data_horario = self.extract_data_script_html(script)

        return self.set_data_by_dia(modulo_hora, data_horario)

    def extract_data_script_html(self, script):
        for s in script:
            if "fill_horario([{" in s.text:
                sSubCadena = str(s)[
                    str(s).find('['):str(s).find(']')+1
                ]

        return json.loads(sSubCadena)

    def set_data_by_dia(self, modulo_hora, data_hora):
        horario = {
            "LUNES":[],
            "MARTES": [],
            "MIERCOLES": [],
            "JUEVES": [],
            "VIERNES": [],
            "SABADO": []
        }
        for data in data_hora:
            if "LUNES" in data["dia"]:
                data["hora"] = self.get_hora(modulo_hora, data["codmod"])
                horario["LUNES"].append(data)
            if "MARTES" in data["dia"]:
                horario["MARTES"].append(data)
                data["hora"] = self.get_hora(modulo_hora, data["codmod"])
            if "MIERCOLES" in data["dia"]:
                data["hora"] = self.get_hora(modulo_hora, data["codmod"])
                horario["MIERCOLES"].append(data)
            if "JUEVES" in data["dia"]:
                data["hora"] = self.get_hora(modulo_hora, data["codmod"])
                horario["JUEVES"].append(data)
            if "VIERNES" in data["dia"]:
                data["hora"] = self.get_hora(modulo_hora, data["codmod"])
                horario["VIERNES"].append(data)
            if "SABADO" in data["dia"]:
                data["hora"] = self.get_hora(modulo_hora, data["codmod"])
                horario["SABADO"].append(data)

        return horario

    def get_hora(self, modulo_hora, codmod):
        for mod in modulo_hora:
                    if codmod in mod["modulo"]:
                        return mod["hora"]

    def get_nombre(self, soup):
        a = soup.find("a", {"id": "userDropdown"})
        nombre_spam = a.find("span").text.replace("\t", "").replace("\n","").strip()
        nombre_list = nombre_spam.replace(" ", ",").split(",")

        nombre = ""
        for n in nombre_list:
            if n:
                nombre = f"{nombre} {n}"

        return nombre.strip()

    def get_data(self):
        soup = self.get_soup(self.URL)
        horario = self.get_horario(soup)
        return horario