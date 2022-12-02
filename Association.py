def Apriori(T, epsilon):
    L = list()
    L.append(ListeElement(T, epsilon))

    k = 1 # On initialise k à 1 pcq L1 va être au rang 0
    while k < len(L[0]) -1:
        #print(f"CreateCandidate(T, {epsilon}, {L}, {k})")
        L.append(CreateCandidate(T, epsilon, L, k))
        k += 1
    return L

def ListeElement(T,epsilon):#je compte le nombre d'éléments et je supprime les éléments de nombre inf à epsilon
    liste = list([x for elem in T for x in elem])
    list2 = list()
    for i in range(len(set([x for elem in T for x in elem]))+1):
        if liste.count(i) >= epsilon:
            list2.append(i)
    return list2

def EvalCandidate(T, epsilon, c): #teste les couples (tuples) pour voir si ce sont de bon candidats | FONCTIONNELLE EN TEST UNITAIRE
    bonCandidat = False
    compteur = 0
    #for i in T: # On parcourt les différent Ti
    #    if Redundance(i,c): # Si tous les élements du tuple sont dans le Ti alors c'est que le compteur est égale à la longueur du tuple
    #        compteur += 1
    if Redundancy(T,c) >= epsilon: # Test vis-à-vis d'epsilon
        bonCandidat = True
    return bonCandidat

def CreateCandidate(T, epsilon, L, k): # crée les candidats potentiels et fait directement appel à EvalCandidate | FONCTIONNELLE EN TEST UNITAIRE
    c = list() # le fait que c soit un set évite les doublons
    for i in L[k-1]: #On itère sur le premier élément de la liste
        a = list()
        if type(i) != int:
            a.append(i[0])
        else:
            a.append(i)
        for b in L[0]: # On ajoute un élément provenant des singletons intéressants
            if b not in a:
                a.append(b)
            if len(a) == k + 1: # Pour rester dans le domaine des L[k-1] 
                if EvalCandidate(T, epsilon, a) and Redundancy(c,a) == 0: # On test si le couple créer est bon candidat
                    c.append([x for x in a])
                a.pop()
    return c # c contient la liste des tuples bons candidats

def Redundancy(c,a): #Test de la redondance d'une liste avec une autre | FONCTIONNELLE EN TEST UNITAIRE
    compteur = 0
    for i in c: #
        compte = 0
        for j in a: # On parcourt le tuple à tester
            if j in i: # Si un élement du tuple est dans le c[j] on ajoute 1 au compteur
                compte += 1
        if compte == len(a):
            compteur += 1
    return compteur # On retourne le nombre de redondance

T = [[1,2,5], [1,3,5], [1,2], [1,2,3,4,5], [1,2,4,5], [2,3,5], [1,5]]
epsilon = 3
print(Apriori(T,epsilon))

###TEST###

#t = [1,2,3,5]
#L = [t, [1,2],[1,5], [2,5], [3,5]]
#a = (1,7)

#print(Redundance(t,a))
#print(list((1,2)))
#print(EvalCandidate(T, epsilon, (1,2)))
#print(f"CreateCandidate(T, {epsilon}, {L}, 2)")
#print(CreateCandidate(T, epsilon, L, 2))

# L[0] = [1,2,3,5] 
# a = L[0][0]
# donc a = [1]