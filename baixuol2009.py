import requests
import sys
from baixuol2004 import trata_horario
from bs4 import BeautifulSoup
from gera_csv import gera_csv

def processa_rodada(dia, n):
    partidas = []
    data = dia.find("span").get_text()
    jogos = dia.find("tbody").find_all("tr")
    for jogo in jogos:
        partida = {}
        partida['rodada'] = n
        partida['data'] = data
        horario = jogo.find("td", {"class": "hora"}).get_text().split("h")
        partida['hora'] = trata_horario(horario)
        partida['casa'] = jogo.find("td", {"class": "time1"}).get_text().strip()
        partida['fora'] = jogo.find("td", {"class": "time2"}).get_text().strip()
        estadio = jogo.find("td", {"class": "estadio"}).get_text()
        local = jogo.find("td", {"class": "cidade"}).get_text()
        partida['local'] = estadio+" - "+local
        # ['  2 ', ' 1  ']
        gols = jogo.find("td", {"class": "resultado"}).get_text().split('x')
        partida['gols_casa'] = gols[0].strip()
        partida['gols_fora'] = gols[1].strip()
        partidas.append(partida)
    return partidas

def parse_ano(ano):
    partidas = []
    if (ano == 2009):
        diretorio = ""
    else:
        diretorio = "tabela-de-jogos/"
    for i in range(1, 39):
        base = "https://www.uol.com.br/esporte/futebol/campeonatos/brasileiro/{ano}/serie-a/{diretorio}tabela-de-jogos-{rodada}a-rodada.jhtm".format(ano=ano, rodada=i, diretorio=diretorio)
        page = requests.get(base)
        if (page.status_code == 200):
            parser = BeautifulSoup(page.content, 'html.parser')
            rodada = parser.find("div", {"class": "tabelajogo"})
            dias = rodada.find_all("table")
            for dia in dias:
                partidas += processa_rodada(dia, i)
    return partidas

def main():
    ano = int(sys.argv[1])
    if (ano < 2009 or ano > 2011):
        raise Exception('ano inválido: precisa ser entre 2009 e 2011')
    partidas = parse_ano(ano)
    gera_csv(ano, partidas)

main()
