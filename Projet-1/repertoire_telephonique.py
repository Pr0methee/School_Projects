#Projet n°1 NSI Valentin Novo, ****** **

import pickle,os

if not os.path.exists('repertoire.txt'):
    with open('repertoire.txt','wb') as f:
        pickle.dump({},f)

def lecture(item):
    "fonction qui permet de renvoyer le nom de la personne qui possède le numéro ou le numéro de la personne ou tous les conatcts"
    with open("repertoire.txt","rb") as fichier:
        donn = pickle.load(fichier)#charger le fichier
        item = item.replace("+","00")#rendre la recherche possible dans le cas d'un numéro +33,...

        for cle,value in donn.items():
            if cle == item:#si on cherche un nom on renvoie le numéro qui lui est associé
                return value
            elif value == item:#si on cherche un numéro on renvoie le nom
                return cle

        if item.upper() == 'ALL':#si on souhaite avoir tous les contacts
            l = ''
            for cle,val in donn.items():
                l += cle+':'+val+'\n'
            return l#on renvoie un str avec sous la forme:
                    #nom1 : numéro1
                    # nom2 : numéro2
                    # ... 
        else:
            return 'Inconnu'#si on n'a rien trouvé on dit que le numéro ou la personne est inconnu(e)

def ecriture():#creer un nouveau contact
    with open("repertoire.txt","rb") as fichier:#charger le fichier
        donn = pickle.load(fichier)

    name = input("entrez le nom de la personne, <0> Pour quitter")#on demand ele nom

    if name != '0':#si on rentre un nom on demand ele numéro et on converti les + en 00
        num = input("Entrez le numéro de téléphone de cette personne")
        num = num.replace("+","00")

        assert num.isdigit(), "le numéro ne contient pas que des chiffres ! "

        donn[name] = num#on enregistre la personne
        with open("repertoire.txt",'wb') as fichier:
            pickle.dump(donn,fichier)#on sauvegarde le dictionnaire
        return None#on n'a pas quitté
    else:
        return 'quit'#signaler que le programme a été quitté

def supprimer(item):#fonction qui supprime une personne ou la personne associée au numéro entré
    with open('repertoire.txt','rb') as fichier:
        donn = pickle.load(fichier)
    
    for cle, value in donn.items():
        if cle == item or value == item:
            del donn[cle]
            with open('repertoire.txt','wb') as fichier:
                pickle.dump(donn,fichier)
            return ''
    
    if item.upper() == 'ALL':#si on veut supprimer tout le répertoire
        donn = {}
        with open('repertoire.txt','wb') as fichier:
            pickle.dump(donn,fichier)
            return ''
    else:
        return "l'élément à supprimer n'existe pas"
       


def menu():#fonction qui affiche le menu et attend une réponse correcte pour la retourner au programme
    print("0-quitter\n1-écrire dans le répertoire\n2-rechercher dans le repertoire\n3-supprimer quelqu'un du repertoire\nVotre choix ?")
    reponse = input()

    assert reponse.isdigit(), "entrez un nombre"#réponse correcte == un nombre entier 
    assert 0 <= int(reponse) <= 3,"mauvaise entrée"#réponse correcte == un nombre qui renvoie à une action

    return int(reponse)
print(os.getcwd())
while 1:
    try:
        reponse = menu()
        if reponse == 0:#quitter
            break
        elif reponse == 1:#écrire
            while ecriture() == None:
                pass
        elif reponse == 2:#lire
            print("Vous pouvez : \n-rechercher un numéro\n-rechercher une personne\n-afficher tous vos contacts en entrant <all>")
            reponse = input()
            print(lecture(reponse))
        elif reponse == 3:
            print("Entrez le numéro ou la personne à supprimer, vous pouvez effacer tout votre répertoire en entrant <all>")
            reponse = input()
            print(supprimer(reponse))
    except Exception as err:
        raise err
