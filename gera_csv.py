import csv

def gera_csv(ano, partidas):
    colunas = [
        'rodada', 'data', 'hora', 'local',
        'casa', 'fora', 'gols_casa', 'gols_fora'
    ]
    destino = open(str(ano)+'.csv', 'w')
    writer = csv.DictWriter(destino, fieldnames=colunas)
    writer.writeheader()
    for partida in partidas:
        writer.writerow(partida) 
