

#Projet Algorithmique des graphes#

##################################
#    Pierre-Emmanuel Scrève      #
#    Alexandre Mihet             #
#    L2 TD1                      #
##################################

#Importation#


#Initialisations#
chaine = "V 0"  # Texte à rechercher
chaine_2 = 'E '
liste_nom_sta = []
liste_traj = []
liste_lignes = []
liste_pass = []
chemin = []
dico = {}
dico_lignes = {}
dico_sta_nom = {}
dico_nom_code = {}


sta_dep_nom = input("Entrer la station de depart ")
sta_end_nom = input("Entrez la station d'arrivee ")

#Fonctions#

def nom_en_code(sta_dep_nom, sta_end_nom):
    global dico_nom_code
    sta_dep = dico_nom_code[sta_dep_nom]
    sta_end = dico_nom_code[sta_end_nom]
    return sta_dep, sta_end

def verification(chaine):
    with open("metro.txt","r") as fichier:
        with open("test.txt","w") as test:
            for ligne in fichier:
                if chaine in ligne:
                    test.writelines(ligne)
            
            test.close()
        fichier.close()


#NE PAS OUBLIER LES DOCSTRING ET LES COMMENTAIRES

# créer une fonction récursive qui va parcourir les arretes et rappeller la fonction sur les sations reliées en mettant les stations parcourues dans une liste pour savoir si on est déjà passé par là
# mettre les trajets dans des listes de listes pour pouvoir parcorir les listes et pour pouvoir avoir les liaisons lors de l'appel de la fonction ci-dessus
# on peut prouver que chaque ligne de metro est connexe et utiliser le fait qu'elles soient connexes pour proposer des trajets plus rapidement en ne parcorant que la ligne nécéssaire

def nom_en_code(sta_dep_nom, sta_end_nom):
    global dico_nom_code
    sta_dep = dico_nom_code[sta_dep_nom]
    sta_end = dico_nom_code[sta_end_nom]
    sta_dep = str(int(sta_dep))
    sta_end = str(int(sta_end))
    # print(dico_nom_code)
    return sta_dep, sta_end

def trajets(liste_traj, chaine):
    """Permet de mettre les arretes(trajets) dans une liste"""
    iter_ligne = 0
    with open("metro.txt", 'r') as file:
        for ligne in file:
            if chaine in ligne:
                if '#' in ligne:
                    pass
                else:
                    liste_traj.append(ligne.split())
                    liste_traj[iter_ligne][3] = int(liste_traj[iter_ligne][3])
                    liste_traj[iter_ligne].remove('E')
                    iter_ligne+=1
        file.close()
        return liste_traj





def liste_to_dico(liste_traj, dico):
    """transforme la liste des trajets en dictionaire"""
    for i in range(len(liste_traj)):
        if liste_traj[i][0] not in dico :
            dico[liste_traj[i][0]] =  {liste_traj[i][1]: liste_traj[i][2]}
        elif liste_traj[i][0] in dico:
            dico[liste_traj[i][0]].update({liste_traj[i][1]: liste_traj[i][2]})

        if liste_traj[i][1] not in dico:
            dico[liste_traj[i][1]] = ({liste_traj[i][0]: liste_traj[i][2]})
        elif liste_traj[i][1] in dico:
            dico[liste_traj[i][1]].update({liste_traj[i][0]: liste_traj[i][2]})







def verif_connexe(station_d, liste_traj):
    """fonction qui va parcourir toutes les station et les met dans une liste"""
    global liste_pass
    if (len(str(station_d)) > 3) or (len(str(station_d)) < 1):
        print("la station de départ n'existe pas")
    else:
        if station_d not in liste_pass:
            liste_pass.append(station_d)
            for i in range(len(liste_traj)):
                for j in range(len(liste_traj[i])):
                    if liste_traj[i][j] == ('%s' % (station_d)) and j == 0:
                        verif_connexe(liste_traj[i][j+1], liste_traj)
                    if liste_traj[i][j] == ('%s' % (station_d)) and j == 1:
                        verif_connexe(liste_traj[i][j-1], liste_traj)
        else:
            pass


#



def unique(liste = liste_pass):
    """fonction utilisée pour vérifier si le programme qui vérifie la connexité fonctionne"""
    vu = []
    for nombre in liste:
        if nombre in vu:
            print ("Nombre déjà vu!")
        else:
            vu.append(nombre)
    if len(vu) == len(liste):
        print("le graphe est connexe")
    else:
        print("le graphe n'est pas connexe")

#

def dijkstra(dico_traj, source):
    """permet de renvoyer le temps le plus court à partir de la station de départ
    et revoie aussi les precedents de chaque station"""
    assert all(dico_traj[u][v] >= 0 for u in dico_traj.keys() for v in dico_traj[u].keys()) #assert permet de vérifier que tous les poids sont positifs, ce qui est nécessaire pour pouvoir utiliser dijkstra
    precedent = {x:None for x in dico_traj.keys()}
    dejaTrait =  {x:False for x in dico_traj.keys()}
    temps = {x:float('inf') for x in dico_traj.keys()}
    temps[source] = 0
    a_traiter = [(0, str(source))]
    while a_traiter:
        temps_noeud, noeud = a_traiter.pop()
        if dejaTrait[noeud] == False:
            dejaTrait[noeud] = True
            for voisin in dico_traj[noeud].keys():
                temps_voisin = temps_noeud + dico_traj[noeud][voisin]
                if temps_voisin < temps[voisin]:
                    temps[voisin] = temps_voisin
                    precedent[voisin] = noeud
                    a_traiter.append((temps_voisin, voisin))
        a_traiter.sort(reverse = True)
    return temps, precedent





def f_chemin(sta_dep, sta_end, precedent):
    """Nous permet de recreer le chemin 
    a partir du dictionnaire des precedent"""
    global chemin
    chemin.append(sta_end)
    current_station = sta_end
    
    while current_station != sta_dep:
        chemin.append(precedent[current_station])
        current_station = precedent[current_station]
    chemin.reverse()
    return chemin

def metro(liste_lignes, chaine):
    """revoie une liste avec à la ligne , le nom et le code de chaque station"""
    iter_ligne = 0
    with open("metro.txt", 'r') as file:
        for ligne in file:
            if chaine in ligne:
                if '#' in ligne:
                    pass
                else:
                    liste_lignes.append(ligne.split())
                    del liste_lignes[iter_ligne][0]
                    liste_lignes[iter_ligne].reverse()
                    iter_ligne+=1
        
        file.close()
        return liste_lignes


def lignes(liste_lignes, lignes):
    """fonction qui permet de mettre dans un dictionnaire:
        -les trations en tant que clés
        -les lignes ou elles se trouvent en valeur"""
    for i in range(len(liste_lignes)):
        ligne = liste_lignes[i][0]
        station = liste_lignes[i][-1]
        lignes[station] = ligne




def nom_station_dico(liste_lignes, chaine):
    """sert a assigner le code des stations à leur nom en utilisant un dicionnaire"""
    global dico_sta_nom, dico_nom_code
    iter_ligne = 0
    with open("metro.txt", 'r') as file:
        for ligne in file:
            if chaine in ligne:
                if '#' in ligne:
                    pass
                else:
                    liste_lignes.append(ligne.split())
                    del liste_lignes[iter_ligne][0]
                    code = liste_lignes[iter_ligne][0]
                    del liste_lignes[iter_ligne][0]
                    ligne = liste_lignes[iter_ligne][-1]
                    del liste_lignes[iter_ligne][-1]
                    liste_lignes[iter_ligne] = ' '.join(liste_lignes[iter_ligne])
                    dico_nom_code[liste_lignes[iter_ligne]] = code
                    dico_sta_nom[code] = liste_lignes[iter_ligne]
                    iter_ligne+=1
        file.close()
        return dico_sta_nom


def intineraire(chemin):
    """permet , avec la liste des precedents, de reconstituer l'ininéraire le plus court"""
    global dico_lignes, temps, sta_end, dico_sta_nom
    ligne_pre = dico_lignes['%04d' % int(chemin[0])]
    print('Vous etes a', dico_sta_nom['%04d' % int(chemin[0])])
    for i in range(len(chemin)+1):
        if i == len(chemin):
            pass
        else:
            ligne_current = dico_lignes['%04d' % int(chemin[i])]
            #ligne_suivant = dico_lignes['%04d' % int(chemin[i+1])]
            if ligne_current != ligne_pre:
                print('A', dico_sta_nom['%04d' % int (chemin[i])], 'changez et prenez la ligne', ligne_current)
            ligne_pre = ligne_current
    print('Vous devriez arriver à', dico_sta_nom['%04d' % int (chemin[-1])], 'dans ', temps[sta_end]//60, 'minutes')



#Main#


#verification(chaine)
#verif_connexe(sta_dep, liste_traj)
#unique()
trajets(liste_traj, chaine_2)
liste_to_dico(liste_traj, dico)
nom_station_dico(liste_nom_sta, chaine)
sta_dep, sta_end = nom_en_code(sta_dep_nom, sta_end_nom)
temps, precedent = dijkstra(dico, sta_dep)
f_chemin(sta_dep, sta_end, precedent)
metro(liste_lignes, chaine)
lignes(liste_lignes, dico_lignes)

intineraire(chemin)