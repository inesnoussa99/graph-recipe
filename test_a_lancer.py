########################################################
import csv

# Definir ici la fonction calcul_liste_longueurs(liste_paires_depart_arrivee)
# qui lit le fichier 'data_arcs.csv' dans le repertoire courant puis
# calcule la longueur de plus court chemin pour chaque paire
# (depart, arrivee) de la liste liste_paires_depart_arrivee.
# Par convention cette longueur sera egale a None si il n'y a pas
# de chemin de 'depart' a 'arrivee'.
# Les plus courts chemins sont cherches en utilisant seulement les arcs
# 'favorise' du graphe.
# Lorsqu'elle se termine la fonction renvoie la liste des longueurs obtenues.

# Par exemple
# calcul_liste_longueurs([('prunier', 'sauge'), ('cardon', 'menthe'), ('pissenlit', 'trefle blanc')])
# renverra la liste [6, None, 4]

# Il est tout à fait possible de definir d'autres fonctions intermedaires
# pour ce calcul, par exemple pour lire le fichier ou pour calculer un plus
# court chemin pour une seule paire (depart, arrivee).

# A DEFINIR ...

def recup_gauche (ch) : 
    '''Fonction permettant de récupérer l'espèce à gauche dans la ligne de la liste pour une relation entre 2 espèces
    Args:
        ch(str), chaine de caractères de type 'espèce1;favorise;espèce2')
    Return: 
        (str), chaine de caractères 'espèce1'
    '''
    p=ch.find(";")
    return ch[:p]

def recup_droite (ch):
    '''Fonction permettant de récupérer l'espèce à droite dans la ligne de la liste pour une relation entre 2 espèces
    Args:
        ch(str), chaine de caractères de type 'espèce1;favorise;espèce2')
    Return: 
        (str), chaine de caractères 'espèce2'
    '''
    p=ch.find(";")
    ch1=ch[p+1:]
    q=ch1.find(";")
    return ch[q+p+2:]

def recup_fav (ch) :
    '''Fonction permettant de récupérer le verbe de la relation entre 2 espèces pour une ligne de la liste
    Args:
        ch(str), chaine de caractères de type 'espèce1;favorise;espèce2')
    Return: 
        (str), chaine de caractères parmi: 'favorise', 'défavorise', 'attire', 'repousse'
    '''
    p=ch.find(";")
    ch1=ch[p+1:]
    q=ch1.find(";")
    return ch[p+1:q+p+1]

def liste_to_dic (listeCSV) :
    '''Fonction qui permet de tranformer une liste en dictionnaire
    Args:
        listeCSV(list), liste avec les relations entre espèces issue de fichier CSV
    Return: 
        dico(dict), dictionnaire ayant pour clés les espèces et pour valeurs les espèces qu'ils favorisent
    '''
    dico={}
    for i in range (len(listeCSV)) :
        ligne=listeCSV[i][0]
        gauche=recup_gauche(ligne)
        droite=recup_droite(ligne)
        fav=recup_fav(ligne)
        if fav =='favorise':
            dico[gauche]=dico.get(gauche ,[])
            dico[gauche].append(droite)
    return dico

def csv_to_list(nom_fichier, eliminer_entete=True, delimiteur=","):
    '''Fonction permettant de transformer un fichier CSV en liste
    Args:
        ch(str), chaine de caractères de type 'espèce1;favorise;espèce2')
    Return: 
        (str), chaine de caractères parmi: 'favorise', 'défavorise', 'attire', 'repousse'
    '''
    with open(nom_fichier,'r', encoding='utf-8') as f :
        csvReader = csv.reader (f,delimiter =delimiteur )
        liste=[]
        if eliminer_entete :
            csvReader.__next__()
        for row in csvReader :
            liste.append(row)
    return liste 


def BFS_chemin (s_init, adj) :
    '''Fonction qui retourne un dictionnaire qui indique pour chaque espèce quel est son parent dans le sous-graphe des parents
    Args:
        s_init(str), sommet(espèce) de départ
        adj(dict), dictionnaire d'adjacence entre espèces
    Return: 
        dico_parents(dict), dictionnaire des parents des espèces
    '''
    a_traiter=[s_init]
    deja_traites=[]
    dico_parents={}
    dico_parents[s_init] = None
    while a_traiter!=[] :
        s = a_traiter.pop(0)
        deja_traites.append(s)
        if s in adj.keys():
            for s1 in adj[s] :
                if s1 not in deja_traites and s1 not in a_traiter  :
                    a_traiter.append(s1)
                    dico_parents[s1]=s
    return dico_parents


def plus_court_chemin (x,y,dico_parents) :
    '''Fonction qui permet de trouver le plus court chemin 'favorise' entre deux espèces
    Args:
        x(str), espèce de départ
        y(str), espèce d'arrivée
        dico_parents(dict), dictionnaire des parents des espèces
    Return: 
        chem(list), liste des espèces reliant x et y 
    '''
    s=y
    chem = []
    while s!= x and s in dico_parents:
        chem.insert(0,s)
        s=dico_parents[s]
    return chem




def calcul_liste_longueurs(liste_paires_depart_arrivee) :
    longueur=[]
    for paire in liste_paires_depart_arrivee:
        
        x=paire[0]
        y=paire[1]
        liste = csv_to_list(fich_trajets)
        graphe= liste_to_dic (liste )
        dico_parents = BFS_chemin(x, graphe) 
        chem1=plus_court_chemin(x,y,dico_parents)
        if chem1!=[]:
            chemin=[x]+chem1
            longueur.append(len(chemin))
        else:
            longueur.append(None)
    return(longueur)
        
fich_trajets = '/Users/Zekhnini Mimouna/Documents/2A/S1/ISN/PROJET/data_arcs.csv' 
print(calcul_liste_longueurs([('prunier', 'sauge'), ('cardon', 'menthe'), ('pissenlit', 'trefle blanc')]))




# UNE FOIS CETTE FONCTION DEFINIE, VOUS POUVEZ LA TESTER EN EXECUTANT
# DIRECTEMENT LE PROGRAMME CI-DESSOUS.


########################################################
# NE PAS MODIFIER LA PARTIE CI-DESSOUS, SAUF SI VOUS
# ETES DANS LE ROLE D'EVALUATEUR.
# SI VOUS ETES EVALUATEUR, LA SEULE MODIFICATION A APPORTER
# EST DE MODIFIER CI-DESSOUS LA LIGNE QUI INITIALISE LA
# VARIABLE reference_longueurs_chemins_min
# AFIN DE LA RENSEIGNER AVEC LE JEU DE TEST QUI SERA
# MIS A VOTRE DISPOSITION SUR MOODLE.
########################################################

def run_test():
    # Ce programme compare les longueurs des chemins minimaux renvoyées
    # par la fonction calcul_liste_longueurs(liste_paires_depart_arrivee)
    # aux longueurs correctes, stockées ci-dessous comme références
    # dans la variable reference_longueurs_chemins_min.

    # Exemple de petit jeu de test:
    #reference_longueurs_chemins_min = {('prunier', 'sauge'): 6, ('cardon', 'menthe'): None, ('pissenlit', 'trefle blanc'): 4}
    
    # Exemple de jeu de test plus gros:
    reference_longueurs_chemins_min = {('prunier', 'sauge'): 6, ('pissenlit', 'trefle blanc'): 4, ("oeillet d'inde", 'asperge'): None, ('ciboulette chinoise', 'marjolaine'): None, ('trefle blanc', 'panais'): 3, ('melon', 'trefle blanc'): 4, ('piment', 'poivron'): None, ('thym', "rosier d'inde"): 4, ('celeri', 'pissenlit'): 5, ('poivron', 'laitue'): 3, ('lavande', 'topinambour'): 4, ('courge', 'pissenlit'): 5, ('coriandre', 'tournesol'): 4, ('cardon', 'genet'): None, ('menthe', 'piment'): 5, ('mais', 'ciboulette chinoise'): 4, ('cosmos', 'thym'): 3, ("oeillet d'inde", 'patate douce'): None, ('basilic', 'pommier'): 4, ('cornichon', 'patate douce'): None, ('poireau', 'menthe'): None, ("rosier d'inde", 'pasteque'): None, ("oeillet d'inde", 'betterave'): None, ('laitue', 'cornichon'): 3, ('pasteque', 'panais'): 3, ('poivron', 'courgette'): 4, ('origan', 'haricot'): 3, ('carotte', 'groseillier'): 3, ('courge', 'radis'): 3, ('patate douce', 'melisse citronnelle'): 4, ('chou-rave', 'pomme de terre'): None, ('vigne', 'cassis'): 4, ('courgette', 'chenopode blanc'): 5, ('lin', 'cumin'): 4, ('agrume', 'morelle de balbis'): 6, ('cresson', 'sarriette'): 4, ('kiwi', 'artichaut'): 4, ('oignon', 'inule visqueuse'): 4, ('tanaisie commune', 'melisse citronnelle'): 5, ('aneth', 'lavande'): 5, ('anis', 'cumin'): 4, ('chenopode blanc', 'roquette'): None, ('lavande', 'sarriette'): 5, ('origan', 'courgette'): 4, ("oeillet d'inde", 'pomme de terre'): None, ('prunier', 'agrume'): 6, ('kiwi', 'poireau'): 4, ('persil', 'haricot'): 3, ('cerfeuil commun', 'olivier'): 5, ('sarrasin', 'menthe'): None}
    # IMPORTANT: Ce jeu vous permet de réaliser un test, mais c'est un jeu différent
    # qui sera transmis aux évaluateurs.
    
    liste_paires_depart_arrivee = list(reference_longueurs_chemins_min.keys())
    liste_longueurs_reference = list(reference_longueurs_chemins_min.values())
    
    liste_longueurs = calcul_liste_longueurs(liste_paires_depart_arrivee)
    
    nb_differences = 0
    for i, longueur_reference in enumerate(liste_longueurs_reference):
        if longueur_reference != liste_longueurs[i]:
            nb_differences += 1
            print("="*40)
            print(f"DIFFERENCE de nombre d'arcs pour la paire :")
            print(f"    depart={liste_paires_depart_arrivee[i]}")
            print(f"    arrivee={liste_paires_depart_arrivee[i]}")
            print(f"    reference={liste_longueurs_reference[i]}")
            print(f"    longueur={liste_longueurs[i]}")
    
    
    print()
    print("Les longueurs des chemins minimaux utilisant")
    print("les arcs 'favorise' pour les paires du jeu de test")
    if nb_differences == 0:
        print("sont toutes identiques a la version de reference.")
    else:
        print("NE SONT PAS TOUTES IDENTIQUES A LA VERSION DE REFERENCE !!!")

run_test()

