# CONSIGNE : remplacer pass par les instructions attendues
# Les assertions vérifient certains résultats au fur et à mesure


# Une fonction qui peut servir
def affiche(table):
    """Fonction qui affiche les éléments d'une table, un élément par ligne,
    quelle que soit le type de cet élément"""
    for element in table:
        print(element)
    print()    # permet de séparer un peu les affichages


# I) a) Importation de la table et affichage
# écrire le code donné dans l'énoncé

import csv
with open('zoo.csv', 'r', newline='') as csvfile:
    tableReader = csv.reader(csvfile, delimiter=';')
    tableReader.__next__()
    for row in tableReader:
        print(' - '.join(row))


# I) b) Importation de la table et affectation d'une variable

def csv_tuple(nom_fichier):
    """Fonction qui importe un fichier csv sous la forme d'une liste de
    tuples en sautant la ligne d'entêtes"""
    with open(nom_fichier,'r',newline='') as fichier:
        table =csv.reader(fichier,delimiter=";")
        table.__next__()#on saute la 1ère ligne
        liste =[]#on crée un dict qui sera renvoyé une fois qu'il contiendra tous les tuples
        for row in table:#on passe chaque ligne
            liste.append(tuple(row))#la liste apprend chaque ligne en format tuple
        return liste

zoo = csv_tuple('zoo.csv')
assert zoo==[('mammifère', 'Lion'),
             ('mammifère', 'Kangourou'),
             ('mammifère', 'Panda'),
             ('poisson', 'Raie'),
             ('mammifère', 'Gorille'),
             ('mammifère', 'Girafe'),
             ('poisson', 'Requin'),
             ('oiseau', 'Perroquet'),
             ('mammifère', 'Girafe'),
             ('oiseau', 'Autruche'),
             ('mammifère', 'Panda'),
             ('reptile', 'Lézard'),
             ('amphibien', 'Crapaud')
             ]
affiche(zoo)


# II) a) Ajout d'un panda

zoo.append(('mammifère','Panda'))#simple append avec la liste

assert zoo==[('mammifère', 'Lion'),
             ('mammifère', 'Kangourou'),
             ('mammifère', 'Panda'),
             ('poisson', 'Raie'),
             ('mammifère', 'Gorille'),
             ('mammifère', 'Girafe'),
             ('poisson', 'Requin'),
             ('oiseau', 'Perroquet'),
             ('mammifère', 'Girafe'),
             ('oiseau', 'Autruche'),
             ('mammifère', 'Panda'),
             ('reptile', 'Lézard'),
             ('amphibien', 'Crapaud'),
             ('mammifère','Panda')
             ]
affiche(zoo)


# II) b) Détection de doublons

def detecte_doublons(table):
    """Fonction qui renvoie True si au moins un doublon est détecté"""
    for obj in table:
        if table.count(obj) >1:#Si obj est présent plus d'une fois dans la table
            return True#on renvoie True. La boucle est automatiquement coupée
    return False

assert detecte_doublons(zoo)
assert not detecte_doublons([('mammifère', 'Lion'),
                               ('poisson', 'Perche'),
                               ('mammifère', 'Panda')
                               ])


# II) c) Suppression de doublons

def supprime_doublons(table):
    """Fonction qui supprime les doublons d'une table"""
    for obj in table:
        if table.count(obj)>1 :#Si l'objet est plusieurs fois dans la table on le suprime
            table.remove(obj)

supprime_doublons(zoo)
assert not detecte_doublons(zoo)
affiche(zoo)


# III) a) Importation de la table (listes) et affectation d'une variable

def csv_liste(nomFichier):
    """Fonction qui importe un fichier csv sous la forme d'une liste de
    listes en sautant la ligne d'entêtes"""
    #la fonction agit exactement comme csv_tuple sauf que les lignes sont en liste
    with open(nomFichier,'r',newline='') as fichier:
        table =csv.reader(fichier,delimiter=";")
        table.__next__()
        liste =[]
        for row in table:
            liste.append(list(row))#la liste apprend chaque ligne en format list
        return liste

zoo = csv_liste('zoo.csv')
assert zoo==[['mammifère', 'Lion'],
             ['mammifère', 'Kangourou'],
             ['mammifère', 'Panda'],
             ['poisson', 'Raie'],
             ['mammifère', 'Gorille'],
             ['mammifère', 'Girafe'],
             ['poisson', 'Requin'],
             ['oiseau', 'Perroquet'],
             ['mammifère', 'Girafe'],
             ['oiseau', 'Autruche'],
             ['mammifère', 'Panda'],
             ['reptile', 'Lézard'],
             ['amphibien', 'Crapaud']
             ]
affiche(zoo)


# III) b) Nommage des animaux

def ajout_nom(table):
    """Fonction qui demande et ajoute un nom à chaque élément de la table"""
    for obj in table:#on passe en revue chaque objet de la table
        print("Donnez un nom à :",obj)
        nom =input()#on demande à l'utilisateur d'entrer le nom
        obj.append(nom)#et on l'ajoute

ajout_nom(zoo)
affiche(zoo)

# IV) Tri de la table suivant un champ

def tri_table(table,i):
    """Fonction qui tri la table en fonction du champ d'indice i"""
    #tri avec l'algorithme donné dans le cours
    for k in range(len(table)):
        position=k
        for j in range(k+1,len(table)):
            if  table[k][i]>table[j][i]:
                position = j
                table[k], table[position] = table[position], table[k]

tri_table(zoo,2)
affiche(zoo)