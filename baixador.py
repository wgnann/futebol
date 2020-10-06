import CBF, UOL4, UOL9
import sys
from gera_csv import gera_csv

def main():
    ano = int(sys.argv[1])
    if (ano >= 2004 and ano <= 2008):
        partidas = UOL4.parse_ano(ano)
    elif (ano >= 2009 and ano <= 2011):
        partidas = UOL9.parse_ano(ano)
    elif (ano >= 2012 and ano <= 2019):
        partidas = CBF.parse_ano(ano)
    else:
        raise Exception('ano inválido: precisa ser entre 2004 e 2019')
    gera_csv(ano, partidas)

if __name__ == "__main__":
    main()
