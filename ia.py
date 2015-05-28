# -*-coding: utf8-*

import constantes as cst

def ia(depart, arrivee, s):
    liste_bloc = cst.liste_bloc_passe_pas
    bloc_tombe = cst.bloc_passe_a_travers

    positions = []
    cpt = 1
    x_m, y_m = depart
    x_p, y_p = arrivee

    if not x_m and not y_m:
        #on fait spawner le monstre
        for i, y in enumerate(s):
            for j, x in enumerate(y):
                if x in bloc_tombe and s[i + 1][j] not in bloc_tombe:
                    x_m, y_m = j * 30, i * 30
                    positions.append((x_m, y_m))

    if x_p < x_m and s[y_m][x_m - 1] not in bloc_tombe:
        if s[y_m + 1][x_m - 1] in bloc_tombe:
            while s[y_m + cpt][x_m - 1] in bloc_tombe:
                positions.append((x_m - 1, y_m + cpt))
                cpt += 1
    if x_p > x_m and s[y_m][x_m + 1] not in bloc_tombe:
        if s[y_m + 1][x_m + 1] in bloc_tombe:
            while s[y_m + cpt][x_m + 1] in bloc_tombe:
                positions.append((x_m + 1, y_m + cpt))
                cpt += 1

    return positions