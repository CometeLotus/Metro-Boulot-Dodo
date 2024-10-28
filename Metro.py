import heapq

def lire_fichier_metro(nom_fichier):
    """
    Lit un fichier contenant des informations sur les stations de métro et les liaisons.
    
    :param nom_fichier: Le nom du fichier à lire.
    :return: Un dictionnaire de stations et un dictionnaire de graphes des liaisons.
    """
    stations = {}
    graph = {}

    with open(nom_fichier, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if parts[0] == 'V':  # Station
                num_station = int(parts[1])
                nom_station = ' '.join(parts[2:-1])  # Nom de la station
                ligne = parts[-1]  # Ligne du métro
                stations[num_station] = (nom_station, ligne)
                graph[num_station] = []
            elif parts[0] == 'E':  # Liaison
                num_station1 = int(parts[1])
                num_station2 = int(parts[2])
                temps = int(parts[3])
                # Ajouter la liaison dans les deux sens (graphe non orienté)
                graph[num_station1].append((num_station2, temps))
                graph[num_station2].append((num_station1, temps))

    return stations, graph

def dijkstra(graph, start, end, stations):
    """
    Calcule le chemin le plus court entre deux stations en minimisant le nombre de changements de ligne.
    
    :param graph: Le graphe des stations.
    :param start: La station de départ.
    :param end: La station d'arrivée.
    :param stations: Dictionnaire des stations.
    :return: Le chemin trouvé et les informations sur le trajet.
    """
    distances = {node: (float('inf'), float('inf')) for node in graph}
    previous_nodes = {node: (None, None) for node in graph}  # (noeud_précédent, ligne_précédente)
    distances[start] = (0, 0)  # (nombre_de_changements, temps)

    # Priority queue : (nombre_de_changements, temps_de_trajet, node, ligne_précédente)
    priority_queue = [(0, 0, start, None)]

    while priority_queue:
        current_changes, current_time, current_node, current_line = heapq.heappop(priority_queue)

        # Si nous atteignons la destination, nous pouvons arrêter
        if current_node == end:
            break

        for neighbor, travel_time in graph[current_node]:
            neighbor_line = stations[neighbor][1]

            # Déterminer le nombre de changements
            new_changes = current_changes + (1 if neighbor_line != current_line else 0)
            new_time = current_time + travel_time
            
            # Comparer les nouvelles distances
            if (new_changes, new_time) < distances[neighbor]:
                distances[neighbor] = (new_changes, new_time)
                previous_nodes[neighbor] = (current_node, neighbor_line)  # Enregistrer la station précédente et la ligne
                heapq.heappush(priority_queue, (new_changes, new_time, neighbor, neighbor_line))

    # Reconstruire le chemin
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous_nodes[current][0] if previous_nodes[current][0] is not None else None

    path.reverse()  # Inverser le chemin
    return path, distances[end]

def trouver_station_par_nom(stations, nom_recherche):
    """
    Recherche le numéro d'une station à partir de son nom.
    
    :param stations: Dictionnaire des stations.
    :param nom_recherche: Nom de la station à rechercher.
    :return: Le numéro de la station ou None si introuvable.
    """
    for num_station, (nom_station, ligne) in stations.items():
        if nom_station.lower() == nom_recherche.lower():
            return num_station
    return None

def afficher_itineraire(stations, path, travel_info):
    """
    Affiche l'itinéraire à suivre entre deux stations.
    
    :param stations: Dictionnaire des stations.
    :param path: Le chemin à afficher.
    :param travel_info: Informations sur le temps de trajet.
    """
    if not path:
        print("Aucun itinéraire trouvé.")
        return

    travel_time = travel_info[1]
    print(f"— Vous êtes à {stations[path[0]][0]}.")

    current_line = stations[path[0]][1]
    previous_station_name = stations[path[0]][0]

    for i in range(1, len(path)):
        station_suivante = stations[path[i]]

        # Vérifiez si la ligne change
        if station_suivante[1] != current_line:
            # Affiche l'instruction de changement de ligne si ce n'est pas la première station
            if previous_station_name != stations[path[0]][0]:  # Ne pas répéter pour la première station
                print(f"— À {previous_station_name}, prenez la ligne {current_line}.")
            current_line = station_suivante[1]  # Mettre à jour la ligne actuelle

        # Mise à jour du nom de la station précédente
        previous_station_name = station_suivante[0]  # Mise à jour pour le prochain affichage

    # Arrivée finale
    print(f"— À {previous_station_name}, prenez la ligne {current_line} direction {stations[path[-1]][0]}.")
    print(f"— Vous devriez arriver à {stations[path[-1]][0]} dans {travel_time // 60} minutes.")

# Chargement des données
stations, graph = lire_fichier_metro("metro.txt")

# Demande de la station de départ et de la station d'arrivée
nom_depart = input("Entrez le nom de la station de départ : ")
start_station = trouver_station_par_nom(stations, nom_depart)

if start_station is None:
    print("Station de départ introuvable.")
else:
    nom_arrivee = input("Entrez le nom de la station d'arrivée : ")
    end_station = trouver_station_par_nom(stations, nom_arrivee)

    if end_station is None:
        print("Station d'arrivée introuvable.")
    else:
        # Calcul du chemin le plus court en minimisant le nombre de changements
        path, travel_info = dijkstra(graph, start_station, end_station, stations)

        # Affichage de l'itinéraire détaillé
        afficher_itineraire(stations, path, travel_info)
