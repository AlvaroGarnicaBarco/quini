import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime
from database import Database


def db_write_partidos(reales: pd.DataFrame, estimados: pd.DataFrame):
    """

    Args:
        reales:
        estimados:

    Returns:

    """
    # database credentials
    load_dotenv()
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    # hora en la que se añaden los datos
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # limpieza de las probabilidades reales y estimadas
    reales.rename({'1': '1_real', 'X': 'x_real', '2': '2_real'}, axis=1, inplace=True)
    estimados.rename({'1': '1_est', 'X': 'x_est', '2': '2_est'}, axis=1, inplace=True)
    partidos = pd.concat([reales, estimados], axis=1)
    partidos[['local', 'visitante']] = partidos.index.str.split(' - ').to_list()

    with Database(dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port) as db:
        for partido in partidos.iterrows():
            to_insert = {'local': partido.local,
                         'visitante': partido.visitante,
                         # 'jornada_id': ,
                         # 'fecha': , # TODO: añadir el horario en scrapping (horarios())
                         # 'competicion': '', # TODO: scrapear competicion en reales_estimados? leerlo de un diccionatio mapping?
                         'prob_real_1': partido.local,
                         'prob_real_x': partido.local,
                         'prob_real_2': partido.local,
                         'prob_est_1': partido.local,
                         'prob_est_x': partido.local,
                         'prob_est_2': partido.local,
                         'fecha_calculo': timestamp,
                         # 'prob_est_1_final': '',
                         # 'prob_est_x_final': '',
                         # 'prob_est_2_final': '',
                         }
            db.insert('partido', partido)


def db_write_jornada():
    pass


if __name__ == "__main__":
    from scrapping import reales_estimados

    _reales, _estimados = reales_estimados('jornada_36')
