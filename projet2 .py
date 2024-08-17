import conversion, pickle, random #modules
import tkinter.messagebox as messagebox #module qui envoie des messages au joueur
from tkinter import * #module de l'interface graphique

tk=Tk()#création de la fenetre
tk.resizable(0,0)#on bloque sa taille, le joueur ne peut pas l'agrandir/la rétrécir
tk.title('Quiz sur les changements de base !')#mettre un titre à la fenetre

rep=''#variable 'rep' pour la réonse de l'utilisateur
def toute_conversion(n,typ):#
    """
    Cette fonction permet de faire n'importe quelle conversion du nombre n\n
    'typ' est donné sous le format base_de_départ->base_d_arrivée
    """
    where = typ.index('-')#place du '-' qui va permettre de connaitre base_de_départ
    where_ = typ.index('>')+1#place du '>' qui va permettre de connaitre base_d_arrivée

    if typ[:where]=='10':#si on part de base 10
        if typ[where+1:]=='C2':#et qu'on va en C2
            new = conversion.C2(int(n),8)#voici le nombre en C2
        else:#et qu'on va dans une autre base
            new = conversion.from_ten(int(n),int(typ[where_:]))#voici le nouveau nombre
    elif typ[:where].isdigit():#si on part d'une base numérique(2,8,16)
        new = conversion.convert(n,int(typ[:where]),int(typ[where_:]))#on fait la conversion
    elif typ[:where] == 'C2':#si on part de C2
        new=conversion.from_C2(n)
    else:#si on manipule avec de l'IEEE754
        if typ[:where]=='float':#on prt de base 10
            new = conversion.to_IEEE754(float(n),'simple')
        else:#on part de l'IEEE754
            new = conversion.from_IEEE754(n)
    return new#on renvoie le nouveau nombre : n de base_de_départ en base_d_arrivée

def set_w_evt(evt):#
    """
    Fonction qui permet de changer la variable nb_question lorsqu'on clique sur <entrée> dans le widget Entry avec la valeur dans le Entry
    """
    n=entry.get()
    global nb_questions
    nb_questions = n

def set_(var_name,value=None,obj=None):#
    """
    Remplace la variable qui a pour nom 'var_name' soit:\n
    -par une valeur
    -par ce qu'il y a dans l'objet 'obj'
    """
    assert type(var_name) ==str,"'var_name' doit être un str avec le nom d'une variable"
    if obj ==None:
        exec("global %s \n%s = '%s'"%(var_name,var_name,value))
    else:
        exec("global %s \n%s = '%s'"%(var_name,var_name,obj.get()))

def existe(filename):#
    """Renvoie True si le fichier filename existe"""
    try:
        with open(filename, "rb") as file:
            return True
    except:
        return False

def menu():#
    """
    Fonction qui propose le menu du jeu.\n
    Attend que le joueur rentre 1 ou 2 et revoie la valeur pour que le programme l'interprette
    """
    btn_creer=Button(tk,text='Créer',command=lambda name='rep',val=1:set_(name,val), width=35,height=35)
    btn_creer.pack(side=LEFT)#Bouton qui permet de lancer la création d'un quiz

    btn_jouer=Button(tk,text='Jouer',command=lambda name='rep',val=2: set_(name,val), width=35,height=35)
    btn_jouer.pack(side=RIGHT)#Bouton qui permet de lancer le jeu

    #de base la variable rep contient un str vide ''
    #on va attendre que rep change avec l'un des boutons
    while rep == '':
        tk.update()#on met à jour l'interface

    #ça y est rep ==1 ou 2
    #on détruit les 2 boutons

    btn_creer.destroy()
    btn_jouer.destroy()
    return int(rep)#on renvoie la réponse en s'assurant que c'est un int

def Créer(file):#
    global entry,nb_questions,title,nombre,rep
    """
    Fonction qui permet à l'utilisateur de creer son propre quiz et l'enregistre dans le fichier file
    """
    #demande le nombre de questions à créer. Le joueur doit rentrer cette information dans un Entry de tkinter
    new_file = []
    nb_questions = ""
    lab=Label(tk,text="Combien de questions voulez-vous créer ? (Entrée pour continuer)")
    lab.pack()
    entry =Entry(tk)
    entry.pack()
    entry.bind_all("<Return>",set_w_evt)
    while not nb_questions.isdigit():#on attend une valeur chiffrée
        tk.update()
    entry.destroy()#on n'a plus besoin de l'entry

    for i in range(0, int(nb_questions)):#on crée autant de questions que ce que l'utilisateur veut
        new_file.append({})
        lab['text']='Choisissez le type de conversion demandé'
        #on demande au joueur de choisir un type de conversion sur lequel va porter la question
        var=StringVar()
        var.set('10->2')
        btns =[Radiobutton(tk,text=j,variable=var,value=j).pack()for j in['10->2','10->8','10->16','10->C2','2->10','2->8','2->16','8->2','8->10','8->16','16->2',
        '16->8','16->10','C2->10','float->IEEE754','IEEE754->float']]
        title=''
        btn = Button(tk,text='Continuer',command=lambda name='title',obj=var :set_(name,obj=obj))
        btn.pack()
        while title == '':
            tk.update()

        new_file[i]["title"] = titres[title]#on donne le nom de la question en fct du choix
        n=tk.children.copy()#on copie le nom de tous les objets présents dans la fenetre
        for obj in n.values():#on passe en revue touts les objets un à un
            obj.destroy()#on supprime l'objet

        #on demande un nombre à convertir
        nombre=''
        lab=Label(tk,text='Entrez le nombre à convertir :')
        lab.pack()
        entry = Entry(tk)
        entry.pack()
        btn = Button(tk,text='continuer',command = lambda name='nombre',obj=entry:set_(name,obj=obj))
        btn.pack()
        n=title.index('-')
        while not conversion.is_of_base(nombre,title[:n]):#on verifie que le nombre donné est bien un nombre de la base choisie
            tk.update()

        new_file[i]['title']+=' :\n'+ nombre#on ajoute au titre le nombre à convertir
        new_file[i]["rep"] = [toute_conversion(nombre,title)]#liste des réponses proposées le programme entre automatiquement la bonne réponse

        for j in range(0, 3):#on demande alors à l'utilisateur d'entrer les fausses
            entry.delete(0,END)
            lab['text']="Entrez une réponse fausse possible :"
            btn['command']=lambda name='rep',obj=entry:set_(name,obj=obj)
            rep = ''
            while rep == '':
                tk.update()
            new_file[i]["rep"].append(rep)

        random.shuffle(new_file[i]["rep"])#on mélange la liste des réponses
        new_file[i]["good"] = new_file[i]['rep'].index(toute_conversion(nombre,title))+1#on trouve ou est la bonne réponse en compte "humain"
        btn.destroy()
        entry.destroy()
        #...et on continue


    with open(file, "wb") as fichier:
        pickle.dump(new_file, fichier)#enfin on enregistre le fichier. ce qu'on enregistre est une liste de dictionnaires

def Type_jouer():#
    """
    Fonction qui renvoie à quel type de jeu le joueur veut jouer :\n
    1> jouer à un quizz pre-fait\n
    2> jouer à un quiz cree aleatoirement par le programme
    """
    global rep
    lab=Label(tk,text="Vous pouvez :")
    lab.pack()
    btn_cree = Button(tk,text="Jouer à un quiz que vous avez créé",command=lambda name='rep',val=1:set_(name,val), width=35,height=35)
    btn_cree.pack(side=LEFT)
    btn_alea = Button(tk,text="Jouer à un quiz aléatoire",command=lambda name='rep',val=2:set_(name,val), width=35,height=35)
    btn_alea.pack(side=RIGHT)
    #on a affiché tous les choix qui sont possible à l'utilisateur
    rep = "-1"
    while rep=='-1':
        tk.update()#on attend la réponse

    btn_alea.destroy()
    btn_cree.destroy()
    lab.destroy()#on détruit tout
    return int(rep)#on renvoie le choix

def Jouer(using_file=False):#
    """
    Fonction qui permet de jouer au quizz.\n
    Si using_file = True c'est qu'on joue a un quiz pre-fait
    """
    global nb,rep
    score = 0
    if using_file:#si on joue au quiz déjà créé :
        with open("Quiz.txt", "rb") as fichier:
            questions = pickle.load(fichier)#on enregistre les questions. c'est une liste de dictionnaires
        lab=Label(tk)
        lab.pack()
        for q in questions:
            lab['text']=q["title"]#on affiche le titre de la question
            n = 1
            btns=[]
            rep = ""
            for r in q["rep"]:#on crée des bouttons correspondants à toutes les réponse proposée
                btns.append(Button(tk,text =r,command = lambda name='rep',value=n:set_(name,value=value)))
                btns[n-1].pack()
                n += 1

            while rep=='':#on attend une réponse de l'utilisateur
                tk.update()

            if int(rep) == q["good"]:#si le joueur a choisi la bonne réponse
                score += 10#on ajoute des points et on colore le fond en vert
                txt = "votre score : %s point(s)"%(score)
                tk['bg']='green'
            else:
                txt = "votre score : %s point(s)\nLa réponse  %s était la bonne"%(score,q['good'])
                tk['bg']='red'#on colore le fond en rouge
            messagebox.showinfo('',txt)#on montre la bonne réponse
            tk['bg']='SystemButtonFace'#on revient à la couleur de fond d'origine
            for obj in btns:
                obj.destroy()#on enlève tous les boutons

    else:#sinon on joue à un quiz aléatoire
        #on va demander le nombre de questions à poser
        nb = "-1"
        lab=Label(tk,text="Sur combien de questions voulez-vous vous testez?")
        lab.pack()
        entry = Entry(tk)
        entry.pack()
        btn =Button(tk,text="C'est parti !",command = lambda name='nb',obj=entry:set_(name,obj=obj))
        btn.pack()
        while not (int(nb) > 0):
            while not nb.isdigit():#on attend un chiffre
                tk.update()
        entry.destroy()#on detruit l'Entry
        btn.destroy()#on detruit le bouton

        #on retient le nombre de questions à poser en int
        nb = int(nb)
        tk.geometry("1500x250")#on change la taille de la fenetre
        for i in range(nb):#on pose les questions
            rep=''
            type_ques = random.randint(0, 2)#on pose au hasard une question ouverte ou fermée. on a plus de chance d' avoir une question fermée qu'ouverte
            if (type_ques == 0):  # on demande une question à réponse ouverte donc on exclu l'IEEE754 pour eviter les erreurs dues aux arrondis
                entry= Entry(tk)#on crée un Entry
                entry.pack()
                btn = Button(tk,text='Confirmer la réponse',command= lambda name='rep',obj=entry:set_(name,obj=obj))#Un bouton pour confirmer la réponse
                btn.pack()
                conversion_a_affectuer = random.choice(liste_questions_ouvertes)#on choisit au hasard un type de conversion à demander
                if "C2" in conversion_a_affectuer:#si c'est par rapport au C2
                    nb_a_convertir = random.randint(-(2 ** 7), 2 ** 7-1)#on choisit un nombre entre -2**7 et 2**7
                    if "from" in conversion_a_affectuer:# on va demander au joueur de convertir de C2 a base 10
                        nb_a_convertir = conversion.C2(nb_a_convertir,8)  
                        lab['text']="Passez %s de C2 à base 10 "%(nb_a_convertir)#on pose la question
                        correct = str(conversion.from_C2(nb_a_convertir))#on enregistre la réponse correcte

                    else:#sinon on demande au joueur de convertir de base 10 à C2
                        correct = conversion.C2(nb_a_convertir,8)#on enregistre la réponse correcte
                        lab['text']="Passez %s de base 10 à C2 sur 8 bits"%(nb_a_convertir)#on pose la question

                elif "ten" in conversion_a_affectuer :#si c'est des changements de bases liés à la base 1à
                    nb_a_convertir = random.randint(15,500)#on choisit un nombre entre 15 et 500 à convertir
                    base = random.choice([2,8,16])#on choisit aléatoirement une base d'arrivée
                    if "to"in conversion_a_affectuer:#on demande au joueur de convertir vers la base 10
                        correct = str(nb_a_convertir)#on enregistre la réponse correcte
                        nb_a_convertir = conversion.from_ten(nb_a_convertir,base)#on passe le nombre dans la base
                        lab['text']= "Passez %s de la base %s à la base 10"%(nb_a_convertir,base)#on affiche la question
                    else:#on demande au joueur de convertir de la base 10 à l'autre base
                        correct = conversion.from_ten(nb_a_convertir,base)#on retient la réponse correcte
                        lab['text']= "Passez %s en base %s"%(nb_a_convertir,base)#on affiche la question
                else:#sinon c'est une conversion entre 2 base autre que 10
                    b=[2,8,16]
                    base1=random.choice(b)
                    b.remove(base1)
                    base2 = random.choice(b)
                    #on choisit les 2 bases

                    nb_a_convertir = conversion.from_ten(random.randint(1,500),base1)#on choisit le nombre à convertir
                    correct = conversion.convert(nb_a_convertir,base1,base2)#on enregistre la bonne réponse
                    lab['text'] = "Passez %s de base %s à base %s"%(nb_a_convertir,base1,base2) #et on pose la question
            else:#question fermée
                conversion_a_affectuer = random.choice(liste_questions_fermees)#on choisit au hasard un type de conversion à demander
                if "C2" in conversion_a_affectuer:#si c'est par rapport au C2
                    nb_a_convertir = random.randint(-(2 ** 7), 2 ** 7-1)#on choisit le nombre
                    v=random.randint(2,5)#on choisit un décalage pour les réponses fausses
                    if "from" in conversion_a_affectuer:# on va demander au joueur de convertir de C2 a base 10
                        reponses=[nb_a_convertir, -nb_a_convertir, round(nb_a_convertir/v),-round(nb_a_convertir/v)]#litse des réponse à proposer 1bonne 3 fausses
                        random.shuffle(reponses)#on mélange la liste
                        correct = reponses.index(nb_a_convertir)+1#on enregistre le n° de la bonne réponse en décompte "humain"
                        nb_a_convertir = conversion.C2(nb_a_convertir,8) 
                        lab['text']= "%s en C2 donne en base 10 : "%(nb_a_convertir)#on pose la question
                    else:#sinon on demande au joueur de convertir de base 10 à C2
                        reponses = [conversion.C2(x,8) for x in [nb_a_convertir, -nb_a_convertir, round(nb_a_convertir/v),-round(nb_a_convertir/v)]]#liste des réponses
                        random.shuffle(reponses)#on les mélange
                        correct = reponses.index(conversion.C2(nb_a_convertir,8))+1#on enregistre la rep. correcte
                        lab['text']= "%s en base 10 donne en C2 : "%(nb_a_convertir)#on pose la question

                elif "ten" in conversion_a_affectuer :
                    nb_a_convertir = random.randint(15,500)#choix du nombre
                    base = random.choice([2,8,16])#de la base
                    if "to"in conversion_a_affectuer:#to_ten =vers base 10
                        reponses =[nb_a_convertir, nb_a_convertir*base, nb_a_convertir-random.randint(-10,-1), nb_a_convertir-random.randint(1,10)]#liste des réponses
                        random.shuffle(reponses)#on la mélange
                        correct = reponses.index(nb_a_convertir)+1#le n° de la réponse correcte
                        nb_a_convertir = conversion.from_ten(nb_a_convertir,base)
                        lab['text']= "%s en base %s donne en base 10 : "%(nb_a_convertir,base)#on pose la question
                    else:#from_ten= de base 10
                        #liste des réponses
                        reponses = [ conversion.from_ten(x,base) for x in [nb_a_convertir, nb_a_convertir*base, nb_a_convertir-random.randint(-10,10), nb_a_convertir-random.randint(11,15)]]
                        random.shuffle(reponses)#on les mélange
                        correct = reponses.index(conversion.from_ten(nb_a_convertir,base))+1#le n° de la rep. correcte
                        lab['text'] = "%s en base 10 donne en base %s : "%(nb_a_convertir,base)#on affiche la question
                elif conversion_a_affectuer == "convert":#conversion entre 2 bases
                    b=[2,8,16]
                    base1=random.choice(b)
                    b.remove(base1)
                    base2 = random.choice(b)
                    #choix des 2 bases

                    n=random.randint(1,500)#choix du nombre
                    nb_a_convertir = conversion.from_ten(n,base1)#nombre à convertir en base1
                    reponses =[conversion.convert(conversion.from_ten(x,base1),base1,base2) for x in [n,n*2,n*8,n+random.randint(1,20)]]#liste des réponses
                    random.shuffle(reponses)#on les mélange
                    correct = reponses.index(conversion.convert(nb_a_convertir,base1,base2))+1#le n° de la réponse correcte
                    lab['text']= "Passez %s de base %s à base %s"%(nb_a_convertir,base1,base2)#on pose la question
                else:#on fait de l'IEEE754
                    random.shuffle(precision)#on mélange la liste des différentes précision-> on choisit la 1ère
                    nb_a_convertir = round(random.uniform(-500,500),3)#on choisit un nombre à virgule entre -500 et 500 avec 3 chiffre après la virgule
                    v=random.uniform(2,5)#pour faire les réponses fausses
                    if "to" in conversion_a_affectuer:#on va demander au joueur de passer un flotant en IEEE757
                        reponses =[conversion.to_IEEE754(x,precision[0]) for x  in[nb_a_convertir,-nb_a_convertir,nb_a_convertir+v,-nb_a_convertir+v]]#liste des rep.
                        random.shuffle(reponses)#on la mélange
                        correct = reponses.index(conversion.to_IEEE754(nb_a_convertir,precision[0]))+1#n° de la rep. correcte
                        lab['text']= "Passez le flotant %s en IEEE754 en %s précision"%(nb_a_convertir,precision[0])#on pose la question
                    else:#on va demander au joueur de passer un IEEE754 en float
                        reponses =[nb_a_convertir ,-nb_a_convertir, nb_a_convertir+v,-(nb_a_convertir+v)]#liste des rep.
                        random.shuffle(reponses)#on les mélanges
                        correct = reponses.index(nb_a_convertir)+1#n° de la rep correcte
                        nb_a_convertir = conversion.to_IEEE754(nb_a_convertir,precision[0])#nombre en IEEE754
                        lab['text']= "Quelle est la valeur décimale du flottant %s en IEEE754 %s precision"%(nb_a_convertir,precision[0])#on pose la question

                btns=[]#liste qui va contenir tous les boutons réponse
                for i in range(4):
                    btns.append(Button(tk,text =reponses[i],command = lambda name='rep',value=i+1:set_(name,value=value)))#nv bouton qui met rep à i+1:le 1er à 1, le 2ème à 2...
                    btns[i].pack()#on l'injecte

            while rep == '':#on attend une réponse
                tk.update()

            if rep == correct or rep == str(correct):#si le joueur a entré la bonne réponse
                tk['bg']='green'#on passe le fond d'écran en vert
                score +=10#on ajoute 10 au score
                txt="votre score : %s point(s)\n"%(score)#on prépare le texte qui lui sera envoyé
            else:#le joueur à entré une mauvaise réponse
                tk['bg']='red'#on passe le fond d'écran en rouge
                if type_ques ==0:
                    txt = "votre score : %s point(s)\nLa réponse était %s"%(score,correct)#on prépare le texte
                else:
                    txt = "votre score : %s point(s)\nLa réponse %s était la bonne"%(score,correct)#on prépare le texte                    

            messagebox.showinfo(message=txt)#on lance une fenetre de dialogue avec le joueur pour lui donner son score (et la bonne réponse)
            tk['bg']='SystemButtonFace'#on revient à la couleur de fond d'origine
            
            #on fait le ménage selon ce qui a été utilisé selon le type de quetsion
            if type_ques == 0:
                entry.destroy()
                btn.destroy()
            else:
                for obj in btns:
                    obj.destroy()

    try:#on met le score sur 1
        score_final = score/(nb*10)
    except:
        score_final = score/(len(questions)*10)

    if score_final == 1:#si on a tout bon
        txt ="C'était parfait !"
    elif score_final ==0:#si on a tout faux
        txt ="...\nVous avez déjà eu un cours sur le changement de base ??"
    else:#sinon
        txt="C'est bien mais vous avez encore quelques progrès à faire !"

    messagebox.showinfo(message=txt)#on lance une boite de dialogue pour montrer le texte

def main():#
    """
    Fonction principale du programme.\n
    Propose le menu\n
    Et agit selon les souhaits de l'utilisateur
    """
    global rep#on va utiliser la variable 'rep' pour obtenir la réponse
    try:
        while 1:
            tk.geometry("500x500")#on fixe la taille de la fenetre à 500 par 500
            n= tk.children.copy()#on sauvegarde tous les widgets qui sont sur la fenetre
            for obj in n.values():#on les passe tous un par un
                obj.destroy()#on les détruits

            rep=''#réinitialisation de la réponse
            if menu() == 1:#on éxecute le menu. Si le joueur veut créer un quizz
                Créer("Quiz.txt")#on le redirige vers la fonction adéquate
            else:#sinon c'est qu'il veut jouer
                if Type_jouer() == 1:#on demande à quel type de jeu il veut jouer. Si il veut jouer à un quizz pré-fait...
                    if existe("Quiz.txt"):#... est que le fichier qui contient le quizz existe
                        Jouer(True)#on joue en utilisant le fichier
                    else:
                        messagebox.showwarning('Quizz non-créé',"Vous n'avez pas encore créé de quiz")#on prévient le joueur qu'il doit commencer par créer un quizz
                else:#sinon c'est que le joueur veut jouer à un quizz aléatoire
                    Jouer()

            #une fois que le joueur a finit de créer/jouer on lui demande si il veut continuer
            if not messagebox.askyesno('Continuer ?',"Vous avez terminé votre partie.\nVoulez-vous continuer ?"):
                tk.destroy()
                break#si il ne veut pas on quitte le programme
    except:
        pass
    messagebox.showinfo('Crédits','Sophan Ly\nAntoine Marlet\nValentin Novo\n1G4')#message de fin


liste_questions_fermees = [ "C2", "from_C2","to_ten", "from_ten", "convert","to_IEEE754","from_IEEE754"]#liste des questions qui peuvent tomber en q. fermées
liste_questions_ouvertes = [ "C2", "from_C2","to_ten", "from_ten", "convert"]#en q. ouvertes
precision=['simple','double','quadruple']#les précision de l'IEEE754

titres={'10->2':"Passez le nombre suivant de base 10 à base 2",'10->8':"Passez le nombre suivant de base 10 à base 8",'10->16':"Passez le nombre suivant de base 10 à base 16",
'10->C2':"Passez le nombre suivant de base 10 en complément à 2",'2->10':"Passez le nombre suivant de base 2 à base 10",'2->8':"Passez le nombre suivant de base 2 à base 8",
'2->16':"Passez le nombre suivant de base 2 à base 16",'8->2':"Passez le nombre suivant de base 8 à base 2",'8->10':"Passez le nombre suivant de base 8 à base 10",
'8->16':"Passez le nombre suivant de base 8 à base 16",'16->2':"Passez le nombre suivant de base 16 à base 2",'16->8':"Passez le nombre suivant de base 16 à base 8",
'16->10':"Passez le nombre suivant de base 16 à base 10",'C2->10':"Passez le nombre de complément à 2 à base 10",'float->IEEE754':"Passer ce flotant en IEEE754 simple précision",
'IEEE754->float':"Passez ce nombre de la norme IEEE754,simple précision à base 10"}#dict qui permet de faire les titres des questions créées par l'utilisateur

main()#on lance le programme
