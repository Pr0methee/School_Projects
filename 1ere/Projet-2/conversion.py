values = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,
          'A':10,'B':11,'C':12,'D':13,'E':14,'F':15}#dictionnaire des valeurs pour les conversions

precisions = {'simple':[1,8,23],
              'double':[1,11,52],
              'quadruple':[1,15,112]}#dictionnaire des précisions avec le nb de bits pour chacune 'p':[s,e,m]

def is_of_base(n,base):
    """
    Vérifie que n est en base 'base'
    """
    if n =='':
        return False
    else:
        try:
            if base =='C2':
                from_C2(n)
                assert len(n)==8
            elif base == 'IEEE754':
                from_IEEE754(n)
            elif base == 'float':
                float(n)
            else:
                to_ten(n,int(base))
            return True
        except:
            return False

def to_ten(n,from_):#fonction qui transforme un nombre de n'importe quelle base en base 10
    assert type(from_) == int and 1<from_<=16, "la base d'origine doit être en format int, et dans [2;16]"
    assert type(n) == str, 'le nombre à convertir doit être une chaine de caractère'
    assert values[max(list(n))] < from_

    l = len(n)
    nb = 0
    for i in range(l):
        nb += values[n[l-(1+i)]] * from_**i         # ajoute chaque valeur avec leur puissance selon leur place dans le nombre, pour le convertir en base 10
    return nb

def from_ten(n,to_):        #fonction de conversion de la base 10 vers n'importe quelle base
    assert (type(n) and type(to_)) == int, "des nombres sont attendus"

    liste_end = []
    q=n
    r=0
    while q != 0:
        r = q%to_       # calcule le reste de la division euclidienne par le nombre de la base choisi
        q = q//to_      #on calcule le quotient de la division euclienne que l'on divise jusqu'à obtenir 0

        for k,v in values.items():
            if v == r:
                liste_end.append(k) # on ajoute les valeurs de k dans la liste : liste_end
                break
    nb = ''
    for i in range(len(liste_end)):
        nb += liste_end[len(liste_end)-1-i]     # on inverse chaques restes des divisions euclidiennes, pour renvoyer le nombre dans la base choisi
    return nb

def convert(n, from_, to_):     # fonction qui renvoie vers la bonne fonction selon la conversion recherchée
    ten = to_ten(n,from_)
    new = from_ten(ten,to_)
    return new

def C2(n, bits):        #fonction conversion d'un décimal en C2
    assert type(n)==int
    assert len(from_ten(abs(n),2))<bits, "erreur dans le nombre à coder"        # il faut que le nombre de bits choisi doit être supérieur au nombre en binaire

    if n >=0:       #pour nombre positif
        nb = from_ten(n,2)  #conversion en base 2
        l = bits-len(nb)
        nb = '0'*l+nb   #inverse chaque 0 en 1 et inversement, pour trouver la valeur en C2
    else:
        nb = from_ten(n+2**(bits),2)    #pour nombre négatif, conversion en base 2 inversion des 1 et 0
    return nb

def from_C2(n): #fonction de conversion d'un nombre C2 en décimal
    assert type(n)==str
    bits = len(n)       #compte le nombre de 1 et 0 pour savoir le nombre de bits
    if n[0] =='0':
        nb = to_ten(n,2)    # pour nombre positif : renvoie vers la fonction de conversion vers base 10
    else:
        nb = to_ten(n,2)-2**bits        # pour nombre négatif : renvoie vers conversion base 10, et soustrait par la puissance du nombre de bits
    return nb

def to_IEEE754(n,precision):    #fonction de conversion d'un nombre décimal en IEEE754
    assert precision == 'simple' or precision == 'double' or precision == 'quadruple'
    assert type(n) == float or type(n) == int
    assert not(0<=n<1)

    info_prec = precisions[precision]
    if n >= 0:      #si le nombre choisi est supérieur ou égal à 0, le bit de signe est 0
        s = '0'
    else:
        s = '1' #sinon le bit de signe est 1
    n=abs(n)
    e = 0
    while 2**e<n:
        e+=1        #détermine l'exposant de la puissance de 2 la plus proche, inférieure  du nombre n
    e-=1    #on enlève 1 à cet exposant

    m_int = n/(2**e)    #on divise le nombre par l'exposant pour trouver ensuite la mantisse
    l=len(str(m_int))
    m_int = round(m_int-1,l)
        #calcule de l'exposant décalé
    e_dec = e+ 2**(info_prec[1]-1)-1    #ajoute l'excédant selon la précision utilisée
    e_dec = from_ten(e_dec,2)   #on convertit ce nombre en binaire
    l = info_prec[1]-len(e_dec)
    e_dec = '0'*l + e_dec   #en fonction de la précision utilisé on rajoute des 0 pour avoir le bon nombre de bits d'exposant

    m=''

    for i in range(1,info_prec[2]+1):       #calcule de la mantisse en fonction de la précision utilisée, on ajoute directement le 1 car il n'est écrit dans le nombre IEEE754
        if 2**-i< m_int:
            m_int -= 2**-i  #on soustrait le nombre de la mantisse pour avoir un nombre >0 et <1
            m+='1' #si le nombre trouvé est <1 on ajoute 1 à la mantisse
        else:
            m+='0'  # si le nombre trouvé est > 0 et <1, on rajoute un 0 dans la mantisse

    return s+e_dec+m        #ensuite on met bout-à-bout chaque morceau de code en commancant par le signe, puis l'exposant décalé et enfin la mantisse

def from_IEEE754(n):        #fonction de conversion d'un nombre IEEE754 en décimal
    assert type(n) == str
    assert len(n) == 32 or len(n) == 64 or len(n) ==128
    assert n.replace('1','').replace('0','') ==''
    if len(n) == 32:    #si la précision choisie est simple, on déduit le nombre de bits de la mantisse et de l'exposant grâce au dictionnaire des précisions au début du programme
        len_s = precisions['simple'][0]
        len_e = precisions['simple'][1]
        len_m = precisions['simple'][2]
    elif len(n) == 64:  #si la précision choisie est double, on déduit le nombre de bits de la mantisse et de l'exposant grâce au dictionnaire des précisions au début du programme
        len_s = precisions['double'][0]
        len_e = precisions['double'][1]
        len_m = precisions['double'][2]
    elif len(n) == 128: #si la précision choisie est quadruple, on déduit le nombre de bits de la mantisse et de l'exposant grâce au dictionnaire des précisions au début du programme
        len_s = precisions['quadruple'][0]
        len_e = precisions['quadruple'][1]
        len_m = precisions['quadruple'][2]

    s = n[:len_s]
    e_dec = n[len_s:len_s+len_e]
    m = n[len_e+len_s:]

    if s == '1':    #si le bit de signe est 1 alors le nombre est négatif
        s =-1
    else:   #sinon le nombre est positif
        s=1

    e = to_ten(e_dec,2) - (2**(len_e-1)-1) #on soustrait l'exposant décalé (convertit en décimal) par l'excédant de la précision choisie

    m_int = 1
    for  i in range(1,len_m+1): #on n'oublie pas le 1, de la mantisse
        if m[i-1] =='1': #on additionne chaque 1 selon leur position derrière la virgule
            m_int += 2**-i

    return s*m_int*2**e # on multiplie chaque morceau de ce chiffre


if __name__ == '__main__':#ce que le programme doit executer lorsqu'il est lance comme programme principal = pas en temps que module
    print("Attention! Ce programme n'est qu'un module du projet 2 !\nOuvrez directement projet2.py ")
