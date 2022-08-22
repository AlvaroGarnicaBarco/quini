import requests
from bs4 import BeautifulSoup
import pandas as pd
from py.variables import *


def horarios():
    """
    función que scrapea los horarios de la jornada
    """
    respuesta = requests.get('https://www.eduardolosilla.es/')
    soup = BeautifulSoup(respuesta.content, 'html.parser')

    if soup.find('h3',
                 class_='c-boleto-multiples-caja-base-header__container__jornada ng-star-inserted').text.strip().replace(
            ' ', '_').lower() != jornada_actual:
        return 'Jornada que se está intentando generar no corresponde a la jornada actual'

    else:
        base = soup.find(id="body")
        partidos = base.find_all('div', class_='c-caja_base__partido u-clearfix ng-star-inserted')

        partido = []
        horario = []

        for i in partidos:
            partido.append(i.find(class_='c-equipos__teams m-short ng-star-inserted').text.strip())
            horario.append(i.find(class_='c-marcador-horario__time__hour').text.strip() + ' - ' + i.find(
                class_='c-marcador-horario__time__day').text.strip())

        return pd.DataFrame({'horario': horario}, index=partido)


def reales_estimados():
    """
    función que scrapea probs reales y estimadas 
    """
    respuesta = requests.get('https://www.eduardolosilla.es/')
    soup = BeautifulSoup(respuesta.content, 'html.parser')

    if soup.find('h3',
                 class_='c-boleto-multiples-caja-base-header__container__jornada ng-star-inserted').text.strip().replace(
            ' ', '_').lower() != jornada_actual:
        return 'Jornada que se está intentando sacar horarios generando no corresponde a la jornada actual'

    else:
        base = soup.find(id="body")
        partidos = base.find_all('div', class_='c-caja_base__partido u-clearfix ng-star-inserted')

        d = {"contador_{}".format(i): [] for i in range(3)}
        for partido in partidos:
            all_probs = partido.find_all(class_='c-boleto-multiples-porcentajes__row u-clearfix ng-star-inserted')

            for idx, tri_prob in enumerate(all_probs[:3]):
                prob = tri_prob.find_all(class_='u-txt-general c-boleto-multiples-porcentajes__row__normal')

                for i in prob:
                    d["contador_{}".format(idx)].append(int(i.text))

        EL = {}
        LAE = {}
        reales = {}

        for idx, i in enumerate(('1', 'X', '2')):
            EL[i] = d["contador_{}".format(0)][idx::3]
            LAE[i] = d["contador_{}".format(1)][idx::3]
            reales[i] = d["contador_{}".format(2)][idx::3]

        EL = pd.DataFrame(EL, index=horarios().index)
        LAE = pd.DataFrame(LAE, index=horarios().index)
        reales = pd.DataFrame(reales, index=horarios().index) / 100
        estimados = round((EL * 0.3 + LAE * 0.7) / 100, 2)
        rentabilidad = (reales / estimados).round(2)
        return reales, estimados, rentabilidad


def premios(jornada):
    """
    función que scrapea los premios de la jornada
    """
    respuesta = requests.get('https://resultados.as.com/quiniela/2020_2021/{}/'.format(jornada))
    soup = BeautifulSoup(respuesta.content, 'html.parser')

    categorias = soup.find_all(class_='row-table-datos')

    premio = []
    for i in categorias[:6]:
        # acertantes.append(i.find(class_='c-marcador-horario__time__hour').text.strip()
        premio.append(i.find(class_='s-tright').text.strip())

    return pd.DataFrame({'aciertos': list(reversed(range(10, 16))), 'premio (€)': premio})
