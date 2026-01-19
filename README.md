PRISONLINK | NEXUS INTELLIGENCE

Analyse avancée des réseaux criminels par co-incarcération.
Détecter les alliances formées dans l'ombre pour anticiper les structures de demain.

PRÉSENTATION

PrisonLink est une plateforme d'intelligence pénitentiaire conçue pour visualiser et analyser les liens sociaux formés entre détenus au cours de leurs séjours en prison. En se basant sur les données de co-incarcération, l'outil génère un graphe relationnel dynamique permettant d'identifier les individus pivots et les réseaux d'influence.

Pourquoi PrisonLink ?

Le crime organisé se structure souvent derrière les barreaux. PrisonLink permet aux analystes de :

Identifier les "influenceurs" (nœuds à haute centralité).

Visualiser les passerelles entre différents centres pénitentiaires.

Filtrer les relations par durée de contact pour distinguer les simples croisements des alliances durables.

FONCTIONNALITÉS CLÉS

Graphe Interactif : Exploration dynamique des connexions (zoom, déplacement, sélection).

Algorithme de Centralité : Calcul automatique d'un score d'influence basé sur la structure du réseau.

Analyse Multi-Centres : Regroupement visuel des détenus par établissement d'origine.

Filtres Dynamiques :

Filtrage par durée minimale de co-habitation (ex: plus de 24h ensemble).

Filtrage par importance (nombre de connexions).

Recherche instantanée par nom ou par type de charge criminelle.

Export de Données : Fonction de capture d'écran intégrée pour sauvegarder les réseaux identifiés.

INSTALLATION ET UTILISATION

Prérequis

Python 3.8 ou version supérieure.

Une base de données au format CSV nommée : données nettoyés.csv

Dépendances

Installez les bibliothèques nécessaires via votre terminal :

pip install pandas networkx

Exécution

Lancez le script principal pour générer l'interface :

python generate_prisonlink.py

Le script produira deux fichiers consultables dans votre navigateur :

index.html (Page d'accueil)

prison_dashboard.html (Interface d'analyse interactive)

MÉTHODOLOGIE TECHNIQUE

1. Détection des chevauchements

Le système calcule pour chaque paire de détenus l'intersection de leurs intervalles de temps de séjour. Seules les relations dépassant un seuil défini (par défaut 24 heures) sont conservées pour éliminer les contacts fortuits et se concentrer sur les relations potentielles.

2. Calcul d'Influence

Le score d'influence est calculé via la "Centralité d'intermédiarité" (Betweenness Centrality). Cet indicateur mesure à quelle fréquence un individu sert de point de passage obligé entre différents groupes du réseau, révélant ainsi les "courtiers en information" ou les leaders de réseaux.

DESIGN ET INTERFACE

L'interface a été conçue pour être à la fois sobre et efficace :

Typographie : Outfit (lisibilité maximale).

Code Couleur : Palette "Police" (Bleus profonds, Gris anthracite) avec des accents Orange pour les alertes.

Ergonomie : Panneau latéral rétractable pour les contrôles et espace central dédié à la visualisation spatiale.

Développé pour l'analyse stratégique des réseaux criminels.
