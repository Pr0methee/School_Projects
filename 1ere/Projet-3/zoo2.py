# CONSIGNE : remplacer pass par les instructions attendues
# Les assertions vérifient certains résultats au fur et à mesure

zoo = [{'espèce': 'Lion', 'nom': 'Simba', 'classe': 'mammifère'},
       {'espèce': 'Kangourou', 'nom': 'Jumper', 'classe': 'mammifère'},
       {'espèce': 'Panda', 'nom': 'Pandi', 'classe': 'mammifère'},
       {'espèce': 'Raie', 'nom': 'Nicola', 'classe': 'poisson'},
       {'espèce': 'Gorille', 'nom': 'Kong', 'classe': 'mammifère'},
       {'espèce': 'Girafe', 'nom': 'Coucou', 'classe': 'mammifère'},
       {'espèce': 'Requin', 'nom': 'Marteau', 'classe': 'poisson'},
       {'espèce': 'Perroquet', 'nom': 'Blu', 'classe': 'oiseau'},
       {'espèce': 'Girafe', 'nom': 'Neck', 'classe': 'mammifère'},
       {'espèce': 'Autruche', 'nom': 'Speedy', 'classe': 'oiseau'},
       {'espèce': 'Panda', 'nom': 'Glass', 'classe': 'mammifère'},
       {'espèce': 'Lézard', 'nom': 'Curieux', 'classe': 'reptile'},
       {'espèce': 'Crapaud', 'nom': 'Prince', 'classe': 'amphibien'}
       ]

# Une fonction qui peut servir
def affiche(table):
    """Fonction qui affiche les éléments d'une table, un élément par ligne,
    quelle que soit le type de cet élément"""
    for element in table:
        print(element)
    print()    # permet de séparer un peu les affichages


# V) a) Importation de la table (dictionnaires) et affectation d'une variable
# Avec csv.reader(), on saute la ligne d'entête, et on définit manuellement les clés

import csv

def csv_dict(nomFichier):
    """Fonction qui importe un fichier csv sous la forme d'une liste de
    dictionnaires en sautant la ligne d'entêtes"""
    with open(nomFichier,'r',newline='') as fichier:
        table =csv.reader(fichier,delimiter=";")
        keys=table.__next__()#on a toutes les clésdu fichier
        print("keys:",keys)
        liste =[]#liste qui sera renvoyée
        for row in table:
            liste.append({
                keys[n]:row[n] for n in range(len(keys))#pour chaque animal, on apprend chaque clé (dans keys) à laquelle on associe la bonne valeur
                })
        return liste

gestion = csv_dict('gestion.csv')
affiche(gestion)

# V) b) Importation de la table (dictionnaires) et affectation d'une variable
# Avec csv.DictReader(), on utilise la ligne d'entête comme clés

def csv_dict2(nomFichier):
    """Fonction qui importe un fichier csv sous la forme d'une liste de
    dictionnaires en utilisant la ligne d'entêtes comme clés"""
    with open(nomFichier,'r') as fichier:
        table = csv.DictReader(fichier,delimiter=";")
        liste=[]#liste qui sera renvoyée
        for row in table:
            liste.append(dict(row))#on transforme cahque ligne en dict dans une liste
        return liste

gestion2 = csv_dict2('gestion.csv')
assert gestion==gestion2
affiche(gestion2)

# VI) Fusion des deux tables

def fusion_tables(zoo,gestion):
    """Fonction qui combine les deux tables en ne gardant que les champs
    'nom', 'espèce', 'lieu' et 'comportement'"""
    table=[]
    for row in gestion:
        ligne=0
        while zoo[ligne]['nom']!=row['nom']:#on cherche le n° de la ligne où apparait l'animal qui porte le nom
            ligne+=1

        #dans notre nv tableau on enregistre un dict avec le nom, l'espèce, le lieu et le comportement de l'animal
        table.append({
            'nom':row['nom'],
            'espèce':zoo[ligne]['espèce'],
            'lieu':row['lieu'],
            'comportement':row['comportement']
        })

    return table

fusion = fusion_tables(zoo,gestion2)
affiche(fusion)

# VII) Filtre d'une table suivant une valeur de champ

def filtre_table(table):
    """Fonction qui renvoir une table avec seulement les animaux n'ayant
    pas un comportement normal"""
    renvoie=[]#liste qui sera renvoyée
    for row in table:
        if row['comportement']!='normal':#si le comportement n'est pas normal on enregistre l'animal dans une liste à renvoyer
            renvoie.append(row)
    return renvoie

problemes = filtre_table(fusion)
affiche(problemes)