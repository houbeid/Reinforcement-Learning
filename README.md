# Reinforcement-Learning
Ce projet est un projet d’intelligence artificielle basé sur le Reinforcement Learning (RL). L’objectif est de créer un agent intelligent capable de contrôler un snake sur un plateau, en apprenant à prendre des décisions optimales pour maximiser ses récompenses et survivre le plus longtemps possible.
1️# Environment / Board

Plateau de jeu de 10x10 cases.

Pommes vertes (2) apparaissent aléatoirement, elles augmentent la longueur du snake lorsqu’il les mange.

Pommes rouges (1) apparaissent aléatoirement, elles diminuent la longueur du snake.

Le snake démarre avec une longueur de 3 cases.

La session se termine si le snake touche un mur, se mord la queue, ou atteint une longueur nulle.

Interface graphique affichant en temps réel le snake et les pommes.

2️# State

Le snake ne voit que 4 directions à partir de sa tête.

Chaque case vue peut contenir : Mur (W), Snake Head (H), Snake Body (S), Green Apple (G), Red Apple (R), ou vide (0).

L’agent prend ses décisions uniquement à partir de cette vision.

3️# Actions

L’agent peut se déplacer dans 4 directions : UP, LEFT, DOWN, RIGHT.

Chaque action est choisie en fonction de l’état perçu par le snake.

4️# Rewards

Les actions sont récompensées pour guider l’apprentissage :

Manger une pomme verte → reward positif

Manger une pomme rouge → reward négatif

Ne rien manger → petit reward négatif

Collision / game over → gros reward négatif

5️# Q-Learning

Implémentation d’un modèle utilisant Q-Learning pour apprendre la meilleure action à prendre dans chaque état.

Supporte Q-table ou Neural Network pour représenter la fonction Q.

Exploration vs Exploitation gérée avec epsilon-greedy.

Possibilité de sauvegarder et charger l’état d’apprentissage pour réutilisation et évaluation.

6️# Fonctionnalités additionnelles

Mode step-by-step pour suivre l’apprentissage en détail.

Option pour désactiver l’apprentissage et tester un modèle déjà entraîné.

Génération de modèles sauvegardés après 1, 10 et 100 sessions pour montrer l’évolution de l’apprentissage.

Technologies :

Python 3

Pygame (GUI)

Numpy (calculs)

Q-Learning (table ou NN)

Objectif final :
Créer un snake intelligent capable de survivre le plus longtemps possible et d’atteindre au moins une longueur de 10 cases, en utilisant uniquement l’apprentissage par renforcement.
