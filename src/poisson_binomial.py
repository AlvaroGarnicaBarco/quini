import numpy as np

from itertools import combinations


def PoiBi(p, k):
    """
    función para el calculo de Poisson Binomial dado unas probabilidades y un numero de aciertos
    """

    if k < 0 or k > len(p):
        return print('Wrong k value given')
    if any((i < 0 or i > 1) for i in p):
        return print('Wrong p value given')

    # if 1 in p:#caso cuando hay p==1

    prob = 0
    for index_variantes in combinations(range(len(p)), len(p) - k):
        no_variantes = [x for i, x in enumerate(p) if i not in index_variantes]
        variantes = [round(1 - x, 10) for i, x in enumerate(p) if i in index_variantes]
        prob += np.prod(no_variantes + variantes)

    return round(prob, 10)

    # else:  #caso cuando no hay p==1

    # def Ti(i):
    # suma = 0
    # for j in range(len(p)):
    # suma += (p[j]/(1-p[j]))**i
    # return suma

    # if k == 0:
    # mult = 1
    # for i in range(len(p)):
    # mult *= (1-p[i])
    # return round(mult,10)
    # else:
    # suma = 0
    # for i in range(1,k+1): #quizas puedo decir q vaya de 2 a k+1 cuando poibi(,0)=0?
    # suma += ((-1)**(i-1)) * PoiBi(p,k-i) * Ti(i)
    # return round((1/k)*suma,20)
