import requests
from bs4 import BeautifulSoup
from lxml import etree

# 1 Variables a utilizar
rut = "13.911.978-9"
password = "20111979"
LOGIN_URL = "https://portal.cftsanagustin.cl/iniciar_sesion"
URL = "https://portal.cftsanagustin.cl/concentracion_notas"
client = requests.Session()

html = client.get(LOGIN_URL).content
soup = BeautifulSoup(html, 'html.parser')
_token = soup.find("input", {"name":"_token"})["value"]

data_form = {
    "_token": _token,
    "rut": rut,
    "password": password
}
client.post(LOGIN_URL, data=data_form)


html = client.get(URL).content
soup = BeautifulSoup(html, 'html.parser')
div_table = soup.find('div', {"id": "n2022-1"})
table =  div_table.find('table')
thead = table.find("thead")
td = thead.find_all("td")
data_head = [j.text for j in td]
thead = table.find("tbody")
tr_body = thead.find_all("tr")
data_body = []
notas_list = []
notas = {}
for tr in tr_body:
    td = tr.find_all("td")
    td_body = [j.text.replace("\t", "").replace("\n","") for j in td] 
    data_body.append(td_body)

for data in data_body:

    cont = 0
    notas = {}
    for dh in data_head:
        notas[dh] = data[cont].strip()
        cont = cont + 1
    notas_list.append(notas)

print(notas_list)