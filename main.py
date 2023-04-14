from src.data.scrapping import reales_estimados
from src.features.build_features import construccion_probabilidades, feature_engineering, calculo_esperanza
import time


def main(jornada: str, recaudacion: float):
    """
    construcción de la tabla base/core a partir de las probabilidades reales y estimadas

    :param jornada: jornada actual, e.g. 'jornada_3'
    :param recaudacion: recaudacion estimada en €
    :return: None, se guardan datos de reales, estimados y df
    """
    print('Scrapeando tablas de reales y estimados...')
    reales, estimados = reales_estimados(jornada)
    print('% reales: \n')
    print(reales)
    print('% estimados: \n')
    print(estimados)

    start_time = time.time()
    df = construccion_probabilidades(reales=reales, estimados=estimados)
    print(f'construccion_probabilidades ejecutado en {round((time.time() - start_time)/60, 2)} min')

    start_time = time.time()
    df = feature_engineering(df, recaudacion)
    print(f'feature_engineering ejecutado en {round((time.time() - start_time)/60, 2)} min')

    start_time = time.time()
    df = calculo_esperanza(df, recaudacion)
    print(f'calculo_esperanza ejecutado en {round((time.time() - start_time)/60, 2)} min')

    print('Guardando datos...')
    reales.to_csv(f'/Users/Alvaro/Desktop/Quiniela/data/reales/22-23/reales_{jornada}')
    estimados.to_csv(f'/Users/Alvaro/Desktop/Quiniela/data/estimados/22-23/estimados_{jornada}')
    df.to_pickle(f'/Users/Alvaro/Desktop/Quiniela/data/dfs/22-23/df_{jornada}.pkl')


if __name__ == "__main__":
    main("jornada_50", 2_600_000)  # TODO: hacerlo parametrizable (__main__.py/run.py?, yaml?), cada vez que quiero ejecutar una joranda
