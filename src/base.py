import pandas as pd
from itertools import product, combinations
from src.my_functions import jugadas_con_premio


def construccion_probabilidades(reales: pd.DataFrame, estimados: pd.DataFrame) -> pd.DataFrame:
    """
    construye el df de probabilidades por jugada dado los datos reales y estimados

    :param reales: pd.DataFrame con las probabilidades reales scrapeadas en reales_estimados()
    :param estimados: pd.DataFrame con las probabilidades estimadas scrapeadas en reales_estimados()
    :return: pd.Dataframe con las probabilidades reales y estimados para cada una de las 3**14 jugadas
    """
    jugadas = [' '.join(i) for i in product("1X2", repeat=14)]

    # Probabilidad de 10, 11, 12, 13 y 14 según estimados
    print('Calculando probabilidades estimadas de 14...')
    probabilidades14est = [a * b * c * d * e * f * g * h * i * j * k * l * m * n for
                           a, b, c, d, e, f, g, h, i, j, k, l, m, n in
                           product(estimados.iloc[0], estimados.iloc[1], estimados.iloc[2], estimados.iloc[3],
                                   estimados.iloc[4], estimados.iloc[5], estimados.iloc[6], estimados.iloc[7],
                                   estimados.iloc[8], estimados.iloc[9], estimados.iloc[10], estimados.iloc[11],
                                   estimados.iloc[12], estimados.iloc[13])]

    zipped = lambda: zip(probabilidades14est,
                         product(estimados.iloc[0], estimados.iloc[1], estimados.iloc[2], estimados.iloc[3],
                                 estimados.iloc[4], estimados.iloc[5], estimados.iloc[6], estimados.iloc[7],
                                 estimados.iloc[8], estimados.iloc[9], estimados.iloc[10], estimados.iloc[11],
                                 estimados.iloc[12], estimados.iloc[13]))

    print('Calculando probabilidades estimadas de 13...')
    probabilidades13est = [
        sum([(prob14 / variante) * (1 - variante) for variante in (a, b, c, d, e, f, g, h, i, j, k, l, m, n)])
        for prob14, (a, b, c, d, e, f, g, h, i, j, k, l, m, n) in zipped()]

    print('Calculando probabilidades estimadas de 12...')
    probabilidades12est = [
        sum([(prob14 / (variante1 * variante2)) * (1 - variante1) * (1 - variante2) for variante1, variante2 in
             combinations([a, b, c, d, e, f, g, h, i, j, k, l, m, n], 2)])
        for prob14, (a, b, c, d, e, f, g, h, i, j, k, l, m, n) in zipped()]

    print('Calculando probabilidades estimadas de 11...')
    probabilidades11est = [
        sum([(prob14 / (variante1 * variante2 * variante3)) * (1 - variante1) * (1 - variante2) * (1 - variante3) for
             variante1, variante2, variante3 in combinations([a, b, c, d, e, f, g, h, i, j, k, l, m, n], 3)])
        for prob14, (a, b, c, d, e, f, g, h, i, j, k, l, m, n) in zipped()]

    print('Calculando probabilidades estimadas de 10...')
    probabilidades10est = [sum([(prob14 / (variante1 * variante2 * variante3 * variante4)) * (1 - variante1) * (
            1 - variante2) * (1 - variante3) * (1 - variante4) for variante1, variante2, variante3, variante4 in
                                combinations([a, b, c, d, e, f, g, h, i, j, k, l, m, n], 4)])
                           for prob14, (a, b, c, d, e, f, g, h, i, j, k, l, m, n) in zipped()]

    # Probabilidad real de 14, 13 y 12
    print('Calculando probabilidades reales de 14...')
    probabilidades14real = [a * b * c * d * e * f * g * h * i * j * k * l * m * n for
                            a, b, c, d, e, f, g, h, i, j, k, l, m, n in
                            product(reales.iloc[0], reales.iloc[1], reales.iloc[2], reales.iloc[3], reales.iloc[4],
                                    reales.iloc[5], reales.iloc[6], reales.iloc[7], reales.iloc[8], reales.iloc[9],
                                    reales.iloc[10], reales.iloc[11], reales.iloc[12], reales.iloc[13])]

    zipped = lambda: zip(probabilidades14real,
                         product(reales.iloc[0], reales.iloc[1], reales.iloc[2], reales.iloc[3], reales.iloc[4],
                                 reales.iloc[5], reales.iloc[6], reales.iloc[7], reales.iloc[8], reales.iloc[9],
                                 reales.iloc[10], reales.iloc[11], reales.iloc[12], reales.iloc[13]))

    print('Calculando probabilidades reales de 13...')
    probabilidades13real = [
        sum([(prob14 / variante) * (1 - variante) for variante in (a, b, c, d, e, f, g, h, i, j, k, l, m, n)])
        for prob14, (a, b, c, d, e, f, g, h, i, j, k, l, m, n) in zipped()]

    print('Calculando probabilidades reales de 12...')
    probabilidades12real = [
        sum([(prob14 / (variante1 * variante2)) * (1 - variante1) * (1 - variante2) for variante1, variante2 in
             combinations([a, b, c, d, e, f, g, h, i, j, k, l, m, n], 2)])
        for prob14, (a, b, c, d, e, f, g, h, i, j, k, l, m, n) in zipped()]

    print('Construyendo DataFrame...')
    d = {'Jugada': jugadas, 'prob_real14': probabilidades14real, 'prob_real13': probabilidades13real,
         'prob_real12': probabilidades12real, 'prob_est14': probabilidades14est, 'prob_est13': probabilidades13est,
         'prob_est12': probabilidades12est, 'prob_est11': probabilidades11est, 'prob_est10': probabilidades10est}

    return pd.DataFrame(d)


def feature_engineering(df: pd.DataFrame, recaudacion) -> pd.DataFrame:
    """
    Añade al df variables de ranking, acertantes esperados y premios esperados

    :param df: pd.DataFrame que debe contener las probs obtenidas de construccion_probabilidades()
    :param recaudacion: recaudacion predicha en €
    :return: df con nuevas variables
    """
    columnas = recaudacion/0.75

    # Ranking por probabilidades reales y estimadas
    df['rank_real14'] = df['prob_real14'].rank(method='first', ascending=False).astype(int)
    df['rank_real13'] = df['prob_real13'].rank(method='first', ascending=False).astype(int)
    df['rank_real12'] = df['prob_real12'].rank(method='first', ascending=False).astype(int)

    df['rank_est14'] = df['prob_est14'].rank(method='first', ascending=False).astype(int)
    df['rank_est13'] = df['prob_est13'].rank(method='first', ascending=False).astype(int)
    df['rank_est12'] = df['prob_est12'].rank(method='first', ascending=False).astype(int)
    df['rank_est11'] = df['prob_est11'].rank(method='first', ascending=False).astype(int)
    df['rank_est10'] = df['prob_est10'].rank(method='first', ascending=False).astype(int)

    # Acertantes esperados por categoría
    df['acertantes_esperados14'] = round(df['prob_est14'] * columnas, 2)
    df['acertantes_esperados13'] = round(df['prob_est13'] * columnas, 4)
    df['acertantes_esperados12'] = round(df['prob_est12'] * columnas, 4)
    df['acertantes_esperados11'] = round(df['prob_est11'] * columnas, 4)
    df['acertantes_esperados10'] = round(df['prob_est10'] * columnas, 4)

    # Premios esperados por categoría # TODO: restar impuestos (20% a partir de 40k)
    df['premio_esperado14'] = round(recaudacion*0.160 / (df['acertantes_esperados14']).apply(lambda x: 1 if x < 1 else x), 2)
    df['premio_esperado13'] = round(recaudacion*0.075 / (df['acertantes_esperados13']).apply(lambda x: 1 if x < 1 else x), 2)
    df['premio_esperado12'] = round(recaudacion*0.075 / (df['acertantes_esperados12']).apply(lambda x: 1 if x < 1 else x), 2)
    df['premio_esperado11'] = round(recaudacion*0.075 / (df['acertantes_esperados11']).apply(lambda x: 1 if x < 1 else x), 2)
    df['premio_esperado10'] = round(recaudacion*0.090 / (df['acertantes_esperados10']).apply(lambda x: 1 if x < 1 else x), 2)

    return df


def calculo_esperanza(df: pd.DataFrame, recaudacion) -> pd.DataFrame:
    """
    Añade al df variables de ranking, acertantes esperados y premios esperados

    :param df: pd.DataFrame que debe contener las variables obtenidas de feature_engineering()
    :param recaudacion: recaudacion predicha en €
    :return: df con nuevas variables
    """
    # Esperanza premio 13, 12
    print('Calculando EM13...')
    df['premio_esperado13_conmigo'] = recaudacion*0.075 / (df['acertantes_esperados13']+1)
    df['probreal14_x_premio_esperado13'] = df.prob_real14 * df.premio_esperado13_conmigo

    # df['premio_esperado12_conmigo'] = recaudacion*0.075 / (df['acertantes_esperados12']+1)
    # df['probreal14_x_premio_esperado12'] = df.prob_real14 * df.premio_esperado12_conmigo

    dict_ = df[['Jugada', 'probreal14_x_premio_esperado13']].set_index('Jugada').to_dict()  # ,'probreal14_x_premio_esperado12'
    em13 = [sum({jugada_: dict_['probreal14_x_premio_esperado13'][jugada_] for jugada_ in jugadas_con_premio(jugada, 13)}.values()) for jugada in df.Jugada]
    # em12 = [sum({jugada_: dict_['probreal14_x_premio_esperado12'][jugada_] for jugada_ in jugadas_con_premio(jugada, 12)}.values()) for jugada in df.Jugada]

    df['EM13'] = em13
    df['rank_EM13'] = df['EM13'].rank(method='first', ascending=False).astype(int)
    # df['EM12'] = em12
    # df['rank_EM12'] = df['EM12'].rank(method='first', ascending=False).astype(int)

    # Esperanza premio 14
    print('Calculando EM14...')
    df['EM14'] = df['prob_real14'] * ((recaudacion*0.16)/ (((recaudacion/0.75)*df['prob_est14'])+1))
    df['rank_EM14'] = df['EM14'].rank(method='first', ascending=False).astype(int)
    df.sort_values('EM14', ascending=False, inplace=True)

    # Esperanza premio 14+13
    df['EM1413'] = df['EM14'] + df['EM13']
    df['rank_EM1413'] = df['EM1413'].rank(method='first', ascending=False).astype(int)

    # Esperanza premio 14+13+12
    # df['EM'] = df['EM14'] + df['EM13'] + df['EM12']
    # df['rank_EM'] = df['EM'].rank(method='first', ascending=False).astype(int)

    df.drop(['premio_esperado13_conmigo', 'probreal14_x_premio_esperado13',
             ], axis=1, inplace=True)  # 'premio_esperado12_conmigo', 'probreal14_x_premio_esperado12'

    return df
