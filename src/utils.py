import pandas as pd
import os
import numpy as np


def number_of_matching_characters(str1, str2):
    str1 = str1.replace(" ", "")
    str2 = str2.replace(" ", "")
    c = 0

    for i in range(len(str1)):
        if str1[i] == str2[i]:
            c += 1
    return c


def top_signos(df, variable_rank, estimados, *args):
    df_ = pd.DataFrame()
    jugadas = df.sort_values(variable_rank).Jugada.str.replace(' ', '')

    for c in args:
        unos = []
        equis = []
        doses = []
        for partido in range(1, 15):
            _ = jugadas[:c].str[(partido - 1):partido].value_counts()
            try:
                unos.append(_['1'])
            except:
                unos.append(0)
            try:
                equis.append(_['X'])
            except:
                equis.append(0)
            try:
                doses.append(_['2'])
            except:
                doses.append(0)
        df_ = pd.concat([df_, pd.DataFrame({'1': unos, 'X': equis, '2': doses}, index=estimados.index)], axis=1)
    df_.columns = pd.MultiIndex.from_product([[f'Top  {arg}' for arg in args], ['1', 'X', '2']])
    return df_


def jugadas_con_premio(jugada, n):
    jugada = jugada.replace(' ', '')

    if n == 12:
        l = []
        for idx, s in enumerate(jugada):
            _ = jugada[idx + 1:]
            if s == '1':
                opc1 = jugada[:idx] + 'X'
                opc2 = jugada[:idx] + '2'
            elif s == 'X':
                opc1 = jugada[:idx] + '1'
                opc2 = jugada[:idx] + '2'
            elif s == '2':
                opc1 = jugada[:idx] + '1'
                opc2 = jugada[:idx] + 'X'

            for idx2, s2 in enumerate(_):
                if s2 == '1':
                    l.append(" ".join(opc1 + _[:idx2] + 'X' + _[idx2 + 1:]))
                    l.append(" ".join(opc2 + _[:idx2] + 'X' + _[idx2 + 1:]))
                    l.append(" ".join(opc1 + _[:idx2] + '2' + _[idx2 + 1:]))
                    l.append(" ".join(opc2 + _[:idx2] + '2' + _[idx2 + 1:]))
                elif s2 == 'X':
                    l.append(" ".join(opc1 + _[:idx2] + '1' + _[idx2 + 1:]))
                    l.append(" ".join(opc2 + _[:idx2] + '1' + _[idx2 + 1:]))
                    l.append(" ".join(opc1 + _[:idx2] + '2' + _[idx2 + 1:]))
                    l.append(" ".join(opc2 + _[:idx2] + '2' + _[idx2 + 1:]))
                elif s2 == '2':
                    l.append(" ".join(opc1 + _[:idx2] + '1' + _[idx2 + 1:]))
                    l.append(" ".join(opc2 + _[:idx2] + '1' + _[idx2 + 1:]))
                    l.append(" ".join(opc1 + _[:idx2] + 'X' + _[idx2 + 1:]))
                    l.append(" ".join(opc2 + _[:idx2] + 'X' + _[idx2 + 1:]))
    elif n == 13:
        l = []
        for idx, s in enumerate(jugada):
            if s == '1':
                j = jugada[:idx] + 'X' + jugada[idx + 1:]
                l.append(" ".join(j))
                j = jugada[:idx] + '2' + jugada[idx + 1:]
                l.append(" ".join(j))
            elif s == 'X':
                j = jugada[:idx] + '1' + jugada[idx + 1:]
                l.append(" ".join(j))
                j = jugada[:idx] + '2' + jugada[idx + 1:]
                l.append(" ".join(j))
            elif s == '2':
                j = jugada[:idx] + '1' + jugada[idx + 1:]
                l.append(" ".join(j))
                j = jugada[:idx] + 'X' + jugada[idx + 1:]
                l.append(" ".join(j))
    return l


def tabla_jugadas(mis_jugadas, estimados):
    """
    función que crea dataframe del porcentaje de jugados
    """
    mis_jugadas = [jugada.replace(' ', '') for jugada in mis_jugadas]

    _1 = []
    _X = []
    _2 = []

    for i in range(14):
        c1 = 0
        cx = 0
        c2 = 0
        for jugada in mis_jugadas:
            if jugada[i] == '1':
                c1 += 1
            elif jugada[i] == 'X':
                cx += 1
            else:
                c2 += 1

        _1.append(c1)
        _X.append(cx)
        _2.append(c2)

    d = {'1': _1, 'X': _X, '2': _2}
    return round(pd.DataFrame(d, index=list(estimados.index.values)) / len(mis_jugadas), 2)


def jugadas_peñas(df: pd.DataFrame, path_to_jugadas: str, n_jornada: str, año: str):
    """
    lee las jugadas de las peñas que estén en la ruta especificada, y añade una columna al df

    :param df: dataframe base de jugadas
    :param path_to_jugadas: ruta que contiene archivos txt con las jugadas de las peñas
    :param n_jornada: número de la jornada (e.g. 1,2,3,4,etc)
    :param año: año de la temporada (si es la temporada 22-23 el año será 2023)
    :return: df base con 2 nuevas columnas,
    """
    all_peñas = os.listdir(path_to_jugadas)
    all_jugadas = []
    nombres_peñas = []
    for peña in all_peñas:
        with open(f'{path_to_jugadas}/{peña}') as file:
            jugadas_peña = file.readlines() 
            jugadas_peña = [" ".join(jugada_peña.rstrip()[:14]) for jugada_peña in jugadas_peña]
        nombres_peñas.extend([peña.split('.')[0].split(f'{n_jornada}_{año}_')[1].replace('_', ' ')]*len(jugadas_peña))
        all_jugadas += jugadas_peña

    print(f'Cruzando {len(all_jugadas)} jugadas, {len(set(all_jugadas))} de ellas únicas, de {len(all_peñas)} peñas diferentes...')
    
    all_jugadas = pd.DataFrame({'jugada': all_jugadas, 'peñas': nombres_peñas})\
                    .groupby('jugada').agg(total_peñas=('peñas', 'count'), peñas=('peñas', lambda x: x.to_list()))
    df = pd.merge(df, all_jugadas, right_index=True, left_on='Jugada', how='left')
    df['total_peñas'] = df['total_peñas'].fillna(0).astype(int)
    df['peñas'] = df['peñas'].fillna(np.nan)
    
    return df


def aciertos_jugada(jugada: str, resultados: dict) -> int:
    """
    calcula el máximo numero de aciertos posibles de una jugada dado el filtro/resultado de signos
    Args:
        jugada: e.g. '1 1 X X 2 X 1 1 1 X 2 X X 2'
        resultados: tiene que tener el formato siguiente, e.g. {'partido1': ['1', 'X'], 'partido2': ['2'], str....}

    Returns:
        número de aciertos
    """
    aciertos = 0

    for signo, posibles_resultados in zip(jugada.replace(' ', ''), resultados.values()):
        if signo in posibles_resultados:
            aciertos += 1

    return aciertos


def aciertos_mis_jugadas(jugadas: list[str], resultados: dict) -> dict:
    """
    calculo el numero de aciertos posibles de 10 o màs de un conjunto de jugadas
    Args:
        jugadas: lista de jugadas
        resultados: tiene que tener el formato siguiente, e.g. {'partido1': ['1', 'X'], 'partido2': ['2'], str....}

    Returns:
        dict con los aciertos de posibles
    """
    aciertos_dict = {14: 0,
                     13: 0,
                     12: 0,
                     11: 0,
                     10: 0}

    for jugada in jugadas:
        aciertos = aciertos_jugada(jugada, resultados)
        if aciertos >= 10:
            aciertos_dict[aciertos] += 1

    return aciertos_dict


# TODO: funcion que coge un df cualqiera lo abre en un gui y el user puede cambiarlo manualmente (lo que hago con estimados)
def manually_update(df: pd.DataFrame) -> pd.DataFrame:
    pass
