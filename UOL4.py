import re
import requests
from bs4 import BeautifulSoup

def trata_horario(horario):
    H = horario[0]
    M = horario[1]
    if (horario[1] == ''):
        M = "00"
    return H+":"+M

def extrai_tecnicos(texto):
    tecnicos = ["N/A", "N/A"]
    i = 0
    for t in texto.contents:
        if "écnico:" in t:
            # Técnico: Levir Culpi
            tmp = t.split(":")
            tecnicos[i] = tmp[1].strip()
            i += 1
    return tecnicos

def encontra_tecnicos(url):
    tecnicos = ["N/A", "N/A"]
    if (url == None):
        # não teve relato de jogo
        return tecnicos
    page = requests.get(url)
    parser = BeautifulSoup(page.content, 'lxml')
    # diversos tratamentos para entrada de dados
    page = str(parser).replace("<b>","").replace("</b>","")
    page = re.sub("Técnico [a-z]", "técnico", page)
    page = page.replace("Técnico ","Técnico: ")
    page = page.replace("Técnco:","Técnico:")
    page = page.replace("Técnico&gt","Técnico:")
    page = page.replace("Técnicos:","Técnico:")
    page = page.replace("Ténico:","Técnico:")
    parser = BeautifulSoup(page, 'lxml')
    texto = parser.find("span", {"class": "noticialink"})
    if (texto == None):
        # página do tipo pelenet
        texto = parser.find("td", {"class": "man"})
        if (texto == None):
            # 2007 em diante
            texto = parser.find("div", {"id": "texto"})
            if (texto == None):
                return tecnicos
    tecnicos = extrai_tecnicos(texto)
    # texto desestruturado
    if (tecnicos[0] == "N/A"):
        blocos = parser.find_all("p")
        for texto in blocos:
            tecnicos = extrai_tecnicos(texto)
            # para no bloco correto
            if (tecnicos[0] != "N/A"):
                break
    return tecnicos

def processa_rodada(rodada, mes, ano):
    partida = {}
    partidas = []
    tabela = rodada.find_all("tr")
    for linha in tabela:
        if (linha.get("id") == "bgListaRodada"):
            # "1ª RODADA"
            numero = linha.get_text().split('ª')[0]
        if (linha.get("id") == "bgListaData"):
            # "Quarta-feira, 21 de abril"
            data = linha.get_text().split()[1]+'/'+str(mes)+'/'+str(ano)
        if (linha.get("id") == "bg"):
            partida['rodada'] = numero
            partida['data'] = data
            dados = linha.find_all("td")
            # "16h" ou "21h45"
            horario = dados[0].get_text().split("h")
            partida['hora'] = trata_horario(horario)
            partida['casa'] = dados[1].get_text()
            partida['fora'] = dados[2].get_text()
            estadio = dados[3].get_text()
            local = dados[4].get_text()
            partida['local'] = estadio+" - "+local
            # ['2 ', ' 2']
            resultado = linha.find("th")
            gols = resultado.get_text().split('x')
            partida['gols_casa'] = gols[0].strip()
            partida['gols_fora'] = gols[1].strip()
            # url fica à direita
            if (len(dados) > 5):
                url = dados[5].find("a")
                if (url != None):
                    url = url.get("href")
            else:
                url = resultado.next.get("href")
            tecnicos = encontra_tecnicos(url)
            partida['tecnico_casa'] = tecnicos[0]
            partida['tecnico_fora'] = tecnicos[1]
            if (tecnicos[0] == "N/A" or tecnicos[1] == "N/A"):
                print(url)
                print("{rodada}, {data}, {casa}, {fora}".format_map(partida))
            partidas.append(partida)
            partida = {}
    return partidas

def parse_ano(ano):
    meses = [
        '', 'jan', 'fev', 'mar', 'abr',
            'mai', 'jun', 'jul', 'ago',
            'set', 'out', 'nov', 'dez'
    ]
    partidas = []
    for mes in range(4, 13):
        base = "https://www.uol.com.br/esporte/futebol/campeonatos/brasileiro/"+str(ano)+"/jog_"+meses[mes]+".jhtm"
        page = requests.get(base)
        if (page.status_code == 200):
            parser = BeautifulSoup(page.content, 'html.parser')
            rodadas = parser.find_all("table", {"width": "450"})
            for rodada in rodadas:
                partidas += processa_rodada(rodada, mes, ano)
    return partidas
