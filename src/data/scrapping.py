import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import warnings


def horarios(jornada_actual):
    """
    función que scrapea los horarios de la jornada
    """
    respuesta = requests.get('https://www.eduardolosilla.es/')
    soup = BeautifulSoup(respuesta.content, 'html.parser')

    if soup.find('h3',
                 class_='c-boleto-multiples-caja-base-header__container__jornada ng-star-inserted').text.strip().replace(' ', '_').lower()\
            != jornada_actual:
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
                 class_='c-boleto-multiples-caja-base-header__container__jornada ng-star-inserted').text.strip().replace(' ', '_').lower() \
            != jornada_actual:
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


class EscrutinioScraper:
    """
    objeto para escrapear el escrutinio
    """
    def __init__(self, driver_path='/Users/Alvaro/Documents/Drivers/chromedriver'):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(service=Service(driver_path), options=options)
        self.driver.get('https://www.eduardolosilla.es/quiniela/ayudas/escrutinio')
        time.sleep(1)

    def cambiar_jornada(self, jornada: int, temporada: str = '22/23') -> None:  # poner la temporada de config
        """
        cambia la jornada y/o la temporada de la tabla de escrutinio
        Args:
            jornada: jornada de la que se quieren los datos
            temporada: temporada de la que se quieren los datos, por defecto es la temporada actual

        Returns:
            None, cambia el filtro de la tabla de escrutinio
        """
        filtros = self.driver.find_elements(By.TAG_NAME, 'app-selector')
        jornadas = filtros[0]
        temporadas = filtros[1]

        try:
            jornadas.find_element(By.XPATH, f"//option[@title='QUINIELA JORNADA {jornada}']").click()
            time.sleep(0.5)
        except NoSuchElementException:
            raise Exception(f'La jornada {jornada} no existe')

        try:
            temporadas.find_element(By.XPATH, f"//option[@title='TEMPORADA {temporada}']").click()
            time.sleep(0.5)
        except NoSuchElementException:
            raise Exception(f'La temporada {temporada} no existe')

    def extraer_datos(self) -> (float, float, dict, dict):
        """
        scrapea los datos del escrutinio (recaudacion, bote, acertantes y premios)

        Returns:
            escrutinio
        """
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        base = soup.find('app-tabla-categorias')

        # recaudacion
        recaudacion = base.find('span', {'class': 'c-tabla-categorias__recaudacion__price'}).text
        recaudacion = float(recaudacion[:-2].replace('.', '').replace(',', '.'))

        # bote
        bote = base.find('span', {'class': 'c-tabla-categorias__bote__price'}).text
        try:
            bote = float(bote[:-2].replace('.', '').replace(',', '.'))
        except ValueError:
            raise Exception(f'La jornada que se ha seleccionado aún no ha empezado')

        # escrutinio
        tabla = base.find('table', {'class': 'c-tabla-categorias__table'})

        acertantes = tabla.find_all('td', {'class': 'c-tabla-categorias__table__category__acertantes'})
        acertantes = {15 - i: int(acertantes_categoria.text.replace('.', '')) for i, acertantes_categoria in enumerate(acertantes[:6])}
        if acertantes[10] == 0:
            warnings.warn("¡Cuidado! La jornada que ha seleccionado aún no ha acabado")

        premios = tabla.find_all('td', {'class': 'c-tabla-categorias__table__category__premio'})
        premios = {15 - i: float(premio_categoria.text[:-2].replace('.', '').replace(',', '.')) for i, premio_categoria in
                   enumerate(premios[:6])}

        return recaudacion, bote, acertantes, premios

    def quit(self):
        self.driver.quit()


def get_escrutinio(jornada: int, temporada: str = '22/23') -> (float, float, dict, dict):
    """
    scrapea los datos del escrutinio dado una jornada y una temporada
    Args:
        jornada: jornada de la que se quieren los datos
        temporada: temporada de la que se quieren los datos, por defecto es la temporada actual

    Returns:
        escrutinio
    """
    my_scraper = EscrutinioScraper()
    try:
        my_scraper.cambiar_jornada(jornada, temporada)
    except StaleElementReferenceException:  # a veces lo tengo que ejecutar 2 veces para que funcione
        my_scraper.cambiar_jornada(jornada, temporada)
    recaudacion, bote, acertantes, premios = my_scraper.extraer_datos()
    my_scraper.quit()

    return recaudacion, bote, acertantes, premios
