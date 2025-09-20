from flask import Flask, request, jsonify, send_file
import io
import numpy as np
from PIL import Image
import random as rd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Etape 0 : on définit les cases à ne pas modifier

def chemin(L):

    i=L[0]
    j=L[1]
    i2=i
    j2=j
    if j>=6:
        if i==24 and j==21:
            j2=20
        elif i==21 and j==19:
            j2=20
            i2=15
        elif i==9 and j==23:
            j2=22
        elif i==9 and j==19:
            j2=18
        elif i==15 and j==17:
            j2=18
            i2=21
        elif i==24 and j==13:
            j2=12
        elif i==24 and j==17:
            j2=16
        elif i==21 and j==15:
            i2=20
        elif i==20 and j==15:
            i2=19
        elif i==19 and j==15:
            i2=18
        elif i==18 and j==15:
            i2=17
        elif i==17 and j==15:
            i2=16
        elif i==7 and j==15:
            i2=5
            j2=16
        elif i==0 and j==15:
            j2=14
        elif i==5 and j==13:
            i2=7
            j2=14
        elif i==5 and j==9:
            i2=7
            j2=10
        elif i==9 and j==7:
            j2=5
        elif i==0 and j==11:
            j2=10
        elif i==7 and j==11:
            i2=5
            j2=12
        elif i==24 and j==9:
            j2=8
            i2=16

        else:
            if j%2==0: #bleu
                j2=j-1
            if j%4==3: #jaune
                j2=j+1
                i2=i-1
            if j%4==1: #jaune
                j2=j+1
                i2=i+1
    else:
        if i==24 and j==21:
            j2=20
        elif i==21 and j==19:
            j2=20
            i2=15
        elif i==9 and j==23:
            j2=22
        elif i==9 and j==19:
            j2=18
        elif i==15 and j==17:
            j2=18
            i2=21
        elif i==24 and j==13:
            j2=12
        elif i==24 and j==17:
            j2=16
        elif i==16 and j==4:
            j2=3
        elif i==21 and j==15:
            i2=20
        elif i==20 and j==15:
            i2=19
        elif i==19 and j==15:
            i2=18
        elif i==18 and j==15:
            i2=17
        elif i==17 and j==15:
            i2=16
        elif i==7 and j==15:
            i2=5
            j2=16
        elif i==0 and j==15:
            j2=14
        elif i==5 and j==13:
            i2=7
            j2=14
        elif i==9 and j==2:
            j2=1
        elif i==5 and j==9:
            i2=7
            j2=10
        elif i==0 and j==11:
            j2=10
        elif i==7 and j==11:
            i2=5
            j2=12
        elif i==24 and j==9:
            j2=8
            i2=16

        elif i==9 and j==7:
            j2=5
        else:
            if j%2==1:
                j2=j-1
            if j==4 or j==0:
                j2=j+1
                i2=i+1
            if j==2:
                j2=j+1
                i2=i-1
    return([i2,j2])

format = [[8,0],[8,1],[8,2],[8,3],[8,4],[8,5],[8,7],[8,8],[7,8],[5,8],[4,8],[3,8],[2,8],[1,8],[0,8],[18,8],[19,8],[20,8],[21,8],[22,8],[23,8],[24,8],[8,17],[8,18],[8,19],[8,20],[8,21],[8,22],[8,23],[8,24]]

IN = [[0,0],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[1,0],[1,6],[2,0],[2,2],[2,3],[2,4],[2,6],[3,0],[3,2],[3,3],[3,4],[3,6],[4,0],[4,2],[4,3],[4,4],[4,6],[5,0],[5,6],[6,0],[6,1],[6,2],[6,3],[6,4],[6,5],[6,6],[18,0],[18,1],[18,2],[18,3],[18,4],[18,5],[18,6],[19,0],[19,6],[20,0],[20,2],[20,3],[20,4],[20,6],[21,0],[21,2],[21,3],[21,4],[21,6],[22,0],[22,2],[22,3],[22,4],[22,6],[23,0],[23,6],[24,0],[24,1],[24,2],[24,3],[24,4],[24,5],[24,6],[0,18],[0,19],[0,20],[0,21],[0,22],[0,23],[0,24],[1,18],[1,24],[2,18],[2,20],[2,21],[2,22],[2,24],[3,18],[3,20],[3,21],[3,22],[3,24],[4,18],[4,20],[4,21],[4,22],[4,24],[5,18],[5,24],[6,18],[6,19],[6,20],[6,21],[6,22],[6,23],[6,24],[6,8],[6,10],[6,12],[6,14],[6,16],[8,6],[10,6],[12,6],[14,6],[18,6],[16,16],[16,17],[16,18],[16,19],[16,20],[17,20],[18,20],[19,20],[20,16],[20,17],[20,18],[20,19],[20,20],[18,18],[17,8],[16,6],[17,16],[18,16],[19,16]] # pixels noirs fixes


IB=[[2,1],[3,1],[4,1],[1,1],[1,2],[1,3],[1,4],[1,5],[2,5],[3,5],[4,5],[5,1],[5,2],[5,3],[5,4],[5,5],[7,0],[7,1],[7,2],[7,3],[7,4],[7,5],[7,6],[7,7],[6,7],[5,7],[4,7],[3,7],[2,7],[1,7],[0,7],[23,1],[22,1],[21,1],[20,1],[19,1],[19,2],[19,3],[19,4],[19,5],[20,5],[21,5],[22,5],[23,5],[23,4],[23,3],[23,2],[17,0],[17,1],[17,2],[17,3],[17,4],[17,5],[17,6],[17,7],[18,7],[19,7],[20,7],[21,7],[22,7],[23,7],[24,7],[0,17],[1,17],[2,17],[3,17],[4,17],[5,17],[6,17],[7,17],[7,18],[7,19],[7,20],[7,21],[7,22],[7,23],[7,24],[1,19],[1,20],[1,21],[1,22],[1,23],[2,23],[3,23],[4,23],[5,23],[5,22],[5,21],[5,20],[5,19],[4,19],[3,19],[2,19],[6,9],[6,11],[6,13],[6,15],[9,6],[11,6],[13,6],[15,6],[17,17],[18,17],[19,17],[19,18],[19,19],[18,19],[17,19],[17,18]] #pixels blancs fixes





# Etape 1_a : on convertit notre texte en codage alpha sur 224 bits car on a choisi le modèle 2-M

def codage_alpha(m : "texte init"):
    L1 = ['0010'] # id de l'alphanumérique
    n = len(m)
    b = bin(n)
    b = b[2:]
    b1 = []
    for i in range (9-len(b)):
        b1.append('0')
    for i in range (len(b)):
        b1.append(b[i])
    for i in range (len(b1)):
        L1.append(b1[i]) # on a ajouté sur 9 bits le nombre de caractères du message

    L = sep_paires(m)
    for i in range (len(L)):
        p = L[i]
        if len(p) == 2 :
            L1.append(codage_bin_alpha(p[0],p[1]))
        else :
            L1.append(codage_bin_alpha(p[0], '@'))
    L1.append('0000')
    return ''.join(L1) # renvoie la suite à rentrer dans le code QR


def sep_paires(m): # sépare le texte en groupes de 2 caractères
    L = []
    n = len(m)
    for i in range (0,n-1,2):
        L.append(m[i] + m[i+1])
    if len(m)%2 != 0 :
        L.append(m[n-1])
    return L


def codage_bin_alpha(l1,l2):
    m1,m2 = dico_alpha(l1),dico_alpha(l2) # on convertit les lettres en leur numéro alpha
    if m2 != '@' :
        s = (45*m1) + m2    # opération de codage alpha
        b = bin(s)
        b = b[2:] # on enlève les 2 premiers caractères qui sont '0b' par ex
        b1 = []
        for i in range (11-len(b)): # on ajoute des 0 pour être sur 11 bits
            b1 += '0'
        for i in range (len(b)):
            b1 += b[i]
        return ''.join(b1)
    else :      # si le dernier couple n'est composé que d'un chiffre
        s = m1
        b = bin(s)
        b = b[2:]
        b1 = []
        for i in range (6-len(b)):
            b1 += '0'
        for i in range(len(b)):
            b1 += b[i]
        return ''.join(b1)


def dico_alpha(l): # on créé un dico représentant l'alphabet alphanumérique
    L = {}
    L1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    for i in range(len(L1)):
            L[L1[i]] = i
    L[" "] = 36
    L["$"] = 37
    L["%"] = 38
    L["*"] = 39
    L["+"] = 40
    L["-"] = 41
    L["."] = 42
    L["/"] = 43
    L[":"] = 44
    L['@'] = '@' # pour l'absence de caractère
    return L[l]


# Etape 1_b : on convertit notre texte en codage octet

def codage_octet(m : "texte init"):
    L1 = ['0100'] # id de l'octet
    n = len(m)
    b = bin(n)
    b = b[2:]
    b1 = []
    for i in range (8-len(b)):
        b1.append('0')
    for i in range (len(b)):
        b1.append(b[i])
    for i in range (len(b1)):
        L1.append(b1[i]) # on a ajouté sur 8 bits le nombre de caractères du message

    L1.append(convert_ascii(m))
    L1.append('0000')
    return ''.join(L1) # renvoie la suite à rentrer dans le code QR


def convert_ascii(l):
    b = ''
    for i in l:
        b1 = '0'
        h = ''.join(hex(ord(i))[2:])
        j = bin(int(h,16))[2:]
        k = 8-len(j)
        b += k*b1 + j
    return b


# Etape 2 : on se donne une liste de 0 et 1 distincts en int (str précédemment)

def str_to_int(b): # convertit les nombres str en nombre int
    L = []
    n = len(b)
    for i in range (n):
        if b[i] == '0':
            L.append(0)
        else:
            L.append(1)
    return L


# Etape 3 : on génère la base du code QR + cf étape 0

def qr(): # création de la base du code qr
    Tab = [[0 for i in range(25)] for i in range(25)]
    for [a,b] in IN:
        Tab[a][b]=1
    for [a,b] in IB:
        Tab[a][b]=0
    return(Tab)


# Etape 4 : on génère le polynôme de correction / Reed-Solomon
# 4.1 : on définit les opérateurs utiles

def XOR(a,b : "a et b sont des entiers en base 10"): # implémentation de l'opération XOR
    r = ['']
    a1,b1 = bin(a),bin(b)
    a2,b2 = [''],['']
    a1,b1 = a1[2:], b1[2:]
    if len(a1) < len(b1):
        for i in range (len(b1)-len(a1)):
            a2[0] += '0'
        for j in range(len(a1)):
            a2[0] += a1[j]
        b2 = b1.split()
    elif len(b1) < len(a1):
        for i in range (len(a1)-len(b1)):
            b2[0] += '0'
        for j in range(len(b1)):
            b2[0] += b1[j]
        a2 = a1.split()
    else :
        a2 = a1.split()
        b2 = b1.split()

    for k in range(len(a2[0])):
        if a2[0][k] == b2[0][k]:
            r[0] += '0'
        else:
            r[0] += '1'
    r = int(r[0],2)
    return(r)


def expo_2(n): # renvoie la puissance de 2 équivalente à n
    a,c = n,0
    while a > 1 :
        a = a // 2
        c += 1
    return c


def pui_2(n):
    return 2**n


def recup_coef_gene(L): # L est la liste de remplissage du code, une liste d'un élément str
    L1 = []
    for i in range(len(L[0])//8 ):
        L1.append(L[0][:8])
        L1[i] = int(L1[i],2)
        L[0] = L[0][8:]
    return L1           # L1 est la liste contenant le coefficient du deg(x) = numero de l'élément


def join_liste_int_10_to_2_str(L):
    n = len(L)
    L1 = ['' for i in range (n)]
    for i in range(n):
        L[i] = bin(L[i])
        L[i] = L[i][2:]
        for j in range(8-len(L[i])):
            L1[i] += '0'
        L1[i] += L[i]
    return ''.join(L1)

# 4.2 : algorithme permettant de se ramener dans GF(256)

def GF_256(a):
# a est un nombre potentiellement strictement plus grand que 255 et on cherche à ce qu'il soit valable dans GF256
    if abs(a) < 2**8:
        return abs(a)
    b,c = abs(a),0
    p = expo_2(b) # on récupère la puissance de 2 de a -> a = 2**p

    while p > 8 :
        c += 1
        p -= 1
    d = XOR(285,2**p)
    n = (2**c)*d

    if n > 255 :
        n1 = 2*d
        for i in range(c-1):
            n1 = 2*n1
            if n1 > 255 :
                n1 = XOR(285,n1)
        return n1
    return n


def dico_GF_256():  # on créé un dictionnaire donnant les valeurs des 255 premières puissances de 2 dans GF256
    D = {}
    D[0] = GF_256(0)
    for i in range (1,255):
        D[i] = GF_256(2**i)
    return D


def trouver_cle(n,D):  # renvoie la valeur initiale d'un élément de GF256
    for cle,val in D.items():
        if val == n:
            return cle



# 4.3 : génération du polynome de correction

def mots_correction(L_msg):   # on génère un 'polynome' de correction
    L_gene = [0,120,104,107,109,102,161,76,3,91,191,147,169,182,194,225,120]    # utilisation du calculateur thonky pour 16 mots de correction
    lm,lg = len(L_msg),len(L_gene)
    L_gene2 = [0 for i in range(lm+lg)]
    D = dico_GF_256()
    L = []
    q = 16      # nombre de mots de code de correction souhaité
    k = abs(lm-lg)+1
    for k in range(lg):
        L_msg.append(0)

    for k in range(lm):
        L_gene.append(0)

    lm,lg = len(L_msg),len(L_gene)
    for j in range (lm-q-1):
        if j == 0 :
            for i in range(j,lm-k-1):
                L_gene2[i] += L_gene[i] + expo_2(L_msg[j])
                L_gene2[i] = GF_256(pui_2(L_gene2[i]%255))
            for i in range(lm)   :
                L_gene2[i] = XOR(L_gene2[i],L_msg[i])
            L_gene2.pop(0)
            k -= 1

        else :
            L_gene3 = [0 for i in range(lm+lg)]
            lg2 = len(L_gene2)
            # if L_gene2[0] == 0:
            #     L_gene2[0] = 1
            s = trouver_cle(L_gene2[0],D)

            for i in range(lg-k-2):

                # print('lgth : ',lg-k-2)
                # print('i : ',i)
                # print(L_gene)
                # print(L_gene[i],'\n',s)
                L_gene3[i] += L_gene[i] + s
                L_gene3[i] = L_gene3[i]%255
                L_gene3[i] = GF_256(pui_2(L_gene3[i]))
            for i in range(lg2-q):
                L_gene3[i] = XOR(L_gene3[i],L_gene2[i])
            L_gene2 = L_gene3
            #if L_gene2 != []:
            L_gene2.pop(0)

    L1 = []

    for i in range (0,q):
        L1.append(L_gene3[i])
    return L1

# Etape 5 : Entrelacement

'''
pas d'entrelacement pour les codes QR de version < 5-M
'''


# Etape 6 : on remplit le code QR

def remplissage(Tab,L): # remplit le code qr en suivant le pattern de remplissage
    #assert len(L) <= 352 # attention au nombre max de caractères possibles
    i=24
    j=24
    for k in range(len(L)):
        Tab[i][j] = L[k]
        i,j=chemin([i,j])
    #print(np.asarray(Tab))
    return Tab


# Etape 7 : on applique un masque

def masques(qr,n):                      # les listes L sont les "id" des masques pour le 2-M
    p = len(qr)
    if n == 0:                          # masque 0
        for i in range(p):              # ligne
            for j in range(p):          # colonne
                if (i+j)%2 == 0:
                    if qr[i][j] == 0:
                        qr[i][j] = 1
                    else :
                        qr[i][j] = 0
        L = ['101010000010010']

    if n == 1:                          # masque 1
        for i in range(p):
            for j in range(p):
                if i%2 == 0:
                    if qr[i][j] == 0:
                        qr[i][j] = 1
                    else :
                        qr[i][j] = 0
        L = ['101000100100101']

    if n == 2:                          # masque 2
        for i in range(p):
            for j in range(p):
                if j%3 == 0:
                    if qr[i][j] == 0:
                        qr[i][j] = 1
                    else :
                        qr[i][j] = 0
        L = ['101111001111100']

    if n == 3:                          # masque 3
        for i in range(p):
            for j in range(p):
                if (i+j)%3 == 0:
                    if qr[i][j] == 0:
                        qr[i][j] = 1
                    else :
                        qr[i][j] = 0
        L = ['101101101001011']


    if n == 4:                          # masque 4
        for i in range(p):
            for j in range(p):
                if (i/2 + j/3)%2 == 0:
                    if qr[i][j] == 0:
                        qr[i][j] = 1
                    else :
                        qr[i][j] = 0
        L = ['100010111111001']


    if n == 5:                          # masque 5
        for i in range(p):
            for j in range(p):
                if (i*j)%2 + (i*j)%3 == 0:
                    if qr[i][j] == 0:
                        qr[i][j] = 1
                    else :
                        qr[i][j] = 0
        L = ['100000011001110']


    if n == 6:                          # masque 6
        for i in range(p):
            for j in range(p):
                if ((i*j)%2 + (i*j)%3)%2 == 0:
                    if qr[i][j] == 0:
                        qr[i][j] = 1
                    else :
                        qr[i][j] = 0
        L = ['100111110010111']


    if n == 7:                          # masque 7
        for i in range(p):
            for j in range(p):
                if ((i+j)%2 + (i*j)%3)%2 == 0:
                    if qr[i][j] == 0:
                        qr[i][j] = 1
                    else :
                        qr[i][j] = 0
        L = ['100101010100000']
    return qr,L

# 7.1 : on ajoute la chaine de format

def patterns(qr,L):
    for i in range(6):
        qr[8][i],qr[24-i][8] = L[i],L[i]

    qr[8][7],qr[18][8] = L[6],L[6]
    qr[8][8],qr[8][17] = L[7],L[7]
    qr[7][8],qr[8][18] = L[8],L[8]
    for i in range(6):
        qr[5-i][8],qr[8][19+i] = L[9+i],L[9+i]
    return qr


def sep2(m): # sépare les caractères de la liste en éléments distincts dans une nouvelle liste
    # on passe de ['01101100'] à ['0','1','1','0','1','1','0','0']
    n = len(m[0])
    L = ['' for i in range(n)]
    for i in range (n):
        L[i] = m[0][i]
    return L

# 7.2 : pénalité de masque

def penal1(qr):
    p = len(qr)

# horizontalement #

    tot1 = 0
    for i in range(p):
        q1 = qr[i][0]
        compteur1 = 1
        for j in range(1,p):
            if j == p-1:
                if qr[i][j] == q1:
                    compteur1 += 1
                    if compteur1 >= 5:
                        compteur1 -= 2
                        #print(f'compteur1 fin : {compteur1}')
                        tot1 += compteur1
                else:
                    if compteur1 >= 5:
                        compteur1 -= 2
                        #print(f'compteur1 fin : {compteur1}')
                        tot1 += compteur1
                q1 = qr[i][j]
                compteur1 = 1

            elif qr[i][j] == q1 :
                compteur1 += 1

            else :
                if compteur1 >= 5:
                    compteur1 -= 2
                    #print(f'compteur1 else : {compteur1}')
                    tot1 += compteur1
                q1 = qr[i][j]
                compteur1 = 1

# verticalement #

    tot2 = 0
    for i in range(p):
        q2 = qr[0][i]
        compteur2 = 1
        for j in range(1,p):
            if j == p-1:
                if qr[j][i] == q2:
                    compteur2 += 1
                    if compteur2 >= 5:
                        compteur2 -= 2
                        #print(f'compteur2 fin : {compteur2}')
                        tot2 += compteur2
                else:
                    if compteur2 >= 5:
                        compteur2 -= 2
                        #print(f'compteur2 fin : {compteur2}')
                        tot2 += compteur2
                q2 = qr[j][i]
                compteur2 = 1

            elif qr[j][i] == q2 :
                compteur2 += 1

            else :
                if compteur2 >= 5:
                    compteur2 -= 2
                    #print(f'compteur2 else : {compteur2}')
                    tot2 += compteur2
                q2 = qr[j][i]
                compteur2 = 1

    #print(f'total : {tot1} + {tot2} = {tot1+tot2}')
    #print(p)
    return tot1 + tot2


def penal2(L):
    p=0
    for i in range(24):
        for j in range(24):
            if L[i][j]==L[i][j+1]==L[i+1][j]==L[i+1][j+1]:
                p+=1
                #print(i,j)
    return p


def penal3(q):
    p = len(q)
    L1 = [0,1,0,0,0,1,0,1,1,1,1]
    L2 = [1,1,1,1,0,1,0,0,0,1,0]
    n = len(L1)
    c1 = 0

# horizontalement #

    for i in range(p):
        for j in range(p-n):
            if q[i][j] == L1[0]:
                if q[i][j+1] == L1[1]:
                    if q[i][j+2] == L1[2]:
                        if q[i][j+3] == L1[3]:
                            if q[i][j+4] == L1[4]:
                                if q[i][j+5] == L1[5]:
                                    if q[i][j+6] == L1[6]:
                                        if q[i][j+7] == L1[7]:
                                            if q[i][j+8] == L1[8]:
                                                if q[i][j+9] == L1[9]:
                                                    if q[i][j+10] == L1[10]:
                                                        c1 += 1
                                                        #print(f'c1h L1 :{c1}',i,j)
            if q[i][j] == L2[0]:
                if q[i][j+1] == L2[1]:
                    if q[i][j+2] == L2[2]:
                        if q[i][j+3] == L2[3]:
                            if q[i][j+4] == L2[4]:
                                if q[i][j+5] == L2[5]:
                                    if q[i][j+6] == L2[6]:
                                        if q[i][j+7] == L2[7]:
                                            if q[i][j+8] == L2[8]:
                                                if q[i][j+9] == L2[9]:
                                                    if q[i][j+10] == L2[10]:
                                                        c1 += 1
                                                        #print(f'c1h L2 :{c1}',i,j)
# verticalement #

    for i in range(p):
        for j in range(p-n+1):
            if q[j][i] == L1[0]:
                if q[j+1][i] == L1[1]:
                    if q[j+2][i] == L1[2]:
                        if q[j+3][i] == L1[3]:
                            if q[j+4][i] == L1[4]:
                                if q[j+5][i] == L1[5]:
                                    if q[j+6][i] == L1[6]:
                                        if q[j+7][i] == L1[7]:
                                            if q[j+8][i] == L1[8]:
                                                if q[j+9][i] == L1[9]:
                                                    if q[j+10][i] == L1[10]:
                                                        c1 += 1
                                                        #print(f'c1v L1 :{c1}',j,i)
            if q[j][i] == L2[0]:
                if q[j+1][i] == L2[1]:
                    if q[j+2][i] == L2[2]:
                        if q[j+3][i] == L2[3]:
                            if q[j+4][i] == L2[4]:
                                if q[j+5][i] == L2[5]:
                                    if q[j+6][i] == L2[6]:
                                        if q[j+7][i] == L2[7]:
                                            if q[j+8][i] == L2[8]:
                                                if q[j+9][i] == L2[9]:
                                                    if q[j+10][i] == L2[10]:
                                                        c1 += 1
                                                        #print(f'c1v L2 :{c1}',j,i)
    return c1


def penal4(qr):
    n=0
    tot=25*25
    for i in range(24):
        for j in range(24):
            if qr[i][j]==1:
                    n+=1
    pourcent=(n/tot)*100
    precedent = pourcent - (pourcent % 5)
    suivant = precedent + 5
    np=(((precedent-50)**2)**0.5)/5
    ns=(((suivant-50)**2)**0.5)/5
    p=min(np,ns)*10
    return p


# Etape 8 : on affiche le code QR

def afficher(M,k): # affiche le tableau sous la forme d'un code qr
    for i in range (len(M[0])):
        for j in  range (len(M[0])):
            if M[i][j] == 1:
                M[i][j] = 0
            else :
                M[i][j] = 1
    return M

def qr2(Tab):   # zones invariantes
    for [a,b] in IN:
        Tab[a][b]=1
    for [a,b] in IB:
        Tab[a][b]=0
    return Tab


def test(qr,z):   # change un certain nombre de pixels du code QR
    p,q = rd.randint(0,24),rd.randint(0,24)
    L = IN+IB+format
    d = int((25**2)*int(z)*10e-3)
    for i in range(d):
        while [p,q] in L:
            p,q = rd.randint(0,24),rd.randint(0,24)
        qr[p][q] = qr[p][q]+1
        L.append([p,q])
    return qr


def main2(k,r,m,z,w):
    if r == 'a':
        l = codage_alpha(m)
    elif r == 'o':
        l = codage_octet(m)
    L = '11101100000100011110110000010001111011000001000111101100000100011110110000010001111011000001000111101100000100011110110000010001111011000001000111101100000100011110110000010001111011000001000111101100'
# si len(l) < 224 on complète avec cette suite qui est équivalente à des 236 et 17
    p = 8-len(l)%8
    for i in range (p):
        l += '0'
    for i in range (224-len(l)):
        l += L[i]
    if k == 0:
        print(f'l : {l}')
    l1 = []
    l1.append(l)
    l2 = mots_correction(recup_coef_gene(l1))
    l2 = join_liste_int_10_to_2_str(l2)
    l += l2
    t = str_to_int(l)
    q = qr()
    r = remplissage(q,t)
    r,L1 = masques(r,k)                      # i est le numéro du masque, on applique le masque
    r = qr2(r)                              # on pose les zones invariantes
    pr = patterns(r,str_to_int(sep2(L1)))    # on insère la chaine d'information de format
    pr = afficher(pr,k)
    return pr


def main(r,m):
    z = 'n' # input('faire un  test de correction : [y] ou [n] -> ')
    w = '0'
    if z == 'y':
        w = '10' # input('quel niveau de test ? [7] ou [15] ou [25] ou [30]')
    for k in range(8):
         return main2(k,r,m,z,w)

def qr_matrix_to_png(matrix, scale=10):
    """Convertit une matrice 0/1 en PNG, en agrandissant chaque module"""
    arr = np.array(matrix, dtype=np.uint8) * 255
    img = Image.fromarray(arr, mode="L")
    img = img.resize((img.size[0]*scale, img.size[1]*scale), Image.NEAREST)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf




@app.route("/generate", methods=["POST"])

def generate_qr():
    """Génère un QR code PNG à partir du texte fourni"""
    data = request.json.get("text", "")
    encod = request.json.get("encod", "o")  # "o" = octet, "a" = alphanumérique
    
    if not data:
        return {"error": "Aucun texte fourni"}, 400
    pr = main(encod, data)
    # Conversion PNG
    buf = qr_matrix_to_png(pr)
    return send_file(buf, mimetype="image/png")

@app.route("/")
def home():
    return {"status": "ok"}
    
if __name__ == "__main__":
    app.run(debug=True)











