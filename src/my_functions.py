def number_of_matching_characters(str1, str2):
    str1 = str1.replace(" ", "")
    str2 = str2.replace(" ", "")
    c = 0   
    
    for i in range(len(str1)):
        if str1[i] == str2[i]:
            c += 1
    return c 

def top_signos(df, variable_rank, *args):
    df_ = pd.DataFrame()
    jugadas = df.sort_values(variable_rank).Jugada.str.replace(' ','')
    
    for c in args:
        unos = []
        equis = []
        doses = []
        for partido in range(1, 15):
            _ = jugadas[:c].str[(partido-1):partido].value_counts()
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
    df_.columns=pd.MultiIndex.from_product([[f'Top  {arg}' for arg in (args)], ['1', 'X', '2']])
    return df_

def jugadas_con_premio(jugada, n):   
    jugada = jugada.replace(' ', '')
    
    if n==12:     
        l = []
        for idx, s in enumerate(jugada):
            _ = jugada[idx + 1:]
            if s=='1':
                opc1 = jugada[:idx] + 'X'
                opc2 = jugada[:idx] + '2'
            elif s=='X':
                opc1 = jugada[:idx] + '1'
                opc2 = jugada[:idx] + '2'
            elif s=='2':
                opc1 = jugada[:idx] + '1'
                opc2 = jugada[:idx] + 'X'

            for idx2, s2 in enumerate(_):
                if s2=='1':
                    l.append(" ".join(opc1 + _[:idx2] + 'X' + _[idx2 + 1:]))
                    l.append(" ".join(opc2 + _[:idx2] + 'X' + _[idx2 + 1:]))
                    l.append(" ".join(opc1 + _[:idx2] + '2' + _[idx2 + 1:]))
                    l.append(" ".join(opc2 + _[:idx2] + '2' + _[idx2 + 1:]))
                elif s2=='X':
                    l.append(" ".join(opc1 + _[:idx2] + '1' + _[idx2 + 1:]))
                    l.append(" ".join(opc2 + _[:idx2] + '1' + _[idx2 + 1:]))
                    l.append(" ".join(opc1 + _[:idx2] + '2' + _[idx2 + 1:]))
                    l.append(" ".join(opc2 + _[:idx2] + '2' + _[idx2 + 1:]))
                elif s2=='2':
                    l.append(" ".join(opc1 + _[:idx2] + '1' + _[idx2 + 1:]))
                    l.append(" ".join(opc2 + _[:idx2] + '1' + _[idx2 + 1:]))
                    l.append(" ".join(opc1 + _[:idx2] + 'X' + _[idx2 + 1:]))
                    l.append(" ".join(opc2 + _[:idx2] + 'X' + _[idx2 + 1:]))
    elif n==13:
        l=[]
        for idx, s in enumerate(jugada):
            if s=='1':
                j = jugada[:idx] + 'X' + jugada[idx + 1:]
                l.append(" ".join(j))
                j = jugada[:idx] + '2' + jugada[idx + 1:]
                l.append(" ".join(j))
            elif s=='X':
                j = jugada[:idx] + '1' + jugada[idx + 1:]
                l.append(" ".join(j))
                j = jugada[:idx] + '2' + jugada[idx + 1:]
                l.append(" ".join(j))
            elif s=='2':
                j = jugada[:idx] + '1' + jugada[idx + 1:]
                l.append(" ".join(j))
                j = jugada[:idx] + 'X' + jugada[idx + 1:]
                l.append(" ".join(j))
    return l 

def tabla_jugadas(mis_jugadas):  
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

        
    d = {'1':_1, 'X':_X, '2':_2}
    return(round(pd.DataFrame(d, index = list(estimados.index.values))/len(mis_jugadas),2))