import requests
from bs4 import BeautifulSoup
import pandas as pd


# TODO: function to scrap recaudacion and jornada, para la temporada meterla como variable global en config? settings?

def horarios(jornada_actual):
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


def reales_estimados(jornada_actual):
    """
    función que scrapea probs reales y estimadas 
    :param jornada_actual:
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

        edu_los = {}
        lae = {}
        reales = {}

        for idx, i in enumerate(('1', 'X', '2')):
            edu_los[i] = d["contador_{}".format(0)][idx::3]
            lae[i] = d["contador_{}".format(1)][idx::3]
            reales[i] = d["contador_{}".format(2)][idx::3]

        edu_los = pd.DataFrame(edu_los, index=horarios(jornada_actual).index)
        lae = pd.DataFrame(lae, index=horarios(jornada_actual).index)
        reales = pd.DataFrame(reales, index=horarios(jornada_actual).index) / 100
        estimados = round((edu_los * 0.4 + lae * 0.6) / 100, 3)

        return reales, estimados


def premios(jornada):
    """
    función que scrapea los premios de la jornada
    """
    respuesta = requests.get(f'https://resultados.as.com/quiniela/2022_2023/{jornada}/')
    soup = BeautifulSoup(respuesta.content, 'html.parser')

    categorias = soup.find_all(class_='row-table-datos')

    premio = []
    for i in categorias[:6]:
        # acertantes.append(i.find(class_='c-marcador-horario__time__hour').text.strip()
        premio.append(i.find(class_='s-tright').text.strip())

    return pd.DataFrame({'aciertos': list(reversed(range(10, 16))), 'premio (€)': premio})
