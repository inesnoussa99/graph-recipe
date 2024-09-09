import csv

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
    


fich_trajets = '/Users/Zekhnini Mimouna/Documents/2A/S1/ISN/PROJET/data_arcs.csv' 

#------PROGRAMME PRINCIPAL---------
 
x="framboisier"
y= "cerisier"
liste = csv_to_list(fich_trajets)
graphe= liste_to_dic (liste )
dico_parents = BFS_chemin(x, graphe)
chem1=plus_court_chemin(x,y,dico_parents)
if chem1!=[]:
    chemin=[x]+chem1
    print(chemin)
else:
    print(None)





