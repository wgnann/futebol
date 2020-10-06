import requests
import sys
from bs4 import BeautifulSoup
from gera_csv import gera_csv

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
            # "16h" ou "21h45"
            horario = linha.find("td", {"class": "col1"}).get_text().split("h")
            H = horario[0]
            M = horario[1]
            if (horario[1] == ''):
                M = "00"
            partida['hora'] = H+":"+M
            partida['casa'] = linha.find("td", {"class": "col2"}).get_text()
            partida['fora'] = linha.find("td", {"class": "col4"}).get_text()
            estadio = linha.find("td", {"class": "col5"}).get_text()
            local = linha.find("td", {"class": "col6"}).get_text()
            partida['local'] = estadio+" - "+local
            placar = linha.find("th", {"class": "col3"}).get_text()
            # ['2 ', ' 2']
            gols = placar.split('x')
            partida['gols_casa'] = gols[0].strip()
            partida['gols_fora'] = gols[1].strip()
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

def main():
    ano = int(sys.argv[1])
    if (ano < 2004 or ano > 2008):
        raise Exception('ano inválido: precisa ser entre 2004 e 2008')
    partidas = parse_ano(ano)
    gera_csv(ano, partidas)

main()
