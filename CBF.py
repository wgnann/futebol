import requests
from bs4 import BeautifulSoup

def filtra_desc(desc):
    datas = []
    locais = []
    for info in desc:
        if ('Jogo:' in info.get_text()):
            datas.append(info)
        if ('Como foi o jogo' in info.get_text() or
            'Detalhes do jogo' in info.get_text()):
            locais.append(info)
    if (len(datas) != len(locais)):
        raise Exception('número distinto de datas e locais')
    return (datas, locais)

def processa_rodada(rodada, n):
    partidas = []
    desc = rodada.find_all("span", {"class": "partida-desc"})
    (datas, locais) = filtra_desc(desc)
    casa = rodada.find_all("div", {"class": "pull-left"})
    fora = rodada.find_all("div", {"class": "pull-right"})
    placar = rodada.find_all("strong", {"class": "partida-horario"})
    for i in range(0, 10):
        partida = {}
        partida['rodada'] = n
        # ['Sáb,', '27/04/2019', '16:00', ... ]
        data = datas[i].get_text().strip().split()
        partida['data'] = data[1]
        partida['hora'] = data[2]
        # ['Morumbi - Sao Paulo - SP', ... ]
        local = locais[i].get_text().strip().split("\n")
        partida['local'] = local[0]
        partida['casa'] = casa[i].find("img").get("alt")
        partida['fora'] = fora[i].find("img").get("alt")
        if ('x' in placar[i].get_text()):
            # ['2 ', ' 0']
            gols = placar[i].get_text().strip().split('x')
        else:
            # WO
            gols = ['-1', '-1']
        partida['gols_casa'] = gols[0].strip()
        partida['gols_fora'] = gols[1].strip()
        partidas.append(partida)
    return partidas

def parse_ano(ano):
    base="https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a/"+str(ano)
    page = requests.get(base)
    parser = BeautifulSoup(page.content, 'html.parser')
    i = 1
    partidas = []
    rodadas = parser.find_all("div", {"class": "aside-content"})
    for rodada in rodadas:
        partidas += processa_rodada(rodada, i)
        i += 1
    return partidas
