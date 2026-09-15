AutoDiag v0.1 — Prototype logiciel de diagnostic automobile
Auteure : Evouna Sonia Ninon
Technologies : Python · OBD2 (cible d'intégration) · JSON
Projet personnel développé en autoformation
Première expérience — v0.1
Cette version constitue une première étape de développement personnel. Elle permet de poser les bases logicielles du projet avant l'intégration de données OBD2 réelles et de capteurs complémentaires.
1. Problématique
AutoDiag explore une solution de diagnostic automobile accessible, pensée initialement pour les chauffeurs de taxi de Yaoundé (Cameroun), pour lesquels la maintenance préventive peut représenter un arbitrage financier important.
L'objectif est d'explorer comment des données issues du véhicule peuvent être transformées en informations simples et exploitables par un utilisateur non technicien.
2. Prototype actuel
La version v0.1 contient le premier cœur logiciel du projet.
Mode 1 — Diagnostic DTC
À partir d'un code défaut DTC, le prototype :
normalise le code saisi ;
recherche sa description dans une base locale ;
attribue un niveau de gravité VERT / ORANGE / ROUGE ;
génère un message compréhensible par l'utilisateur ;
enregistre le diagnostic dans un historique JSON.
Les codes DTC présents dans le prototype sont des codes génériques associés à l'OBD2. Ils constituent une base de démonstration et ne remplacent pas une documentation constructeur ou un diagnostic professionnel.
Mode 2 — Détection précoce d'une anomalie de température
Le prototype accepte une valeur de température moteur et applique des seuils indicatifs :
< 95 °C : VERT ;
95–104 °C : ORANGE ;
≥ 105 °C : ROUGE.
Cette fonction constitue une première approche de détection précoce d'anomalie. Elle ne constitue pas un modèle prédictif validé. Les seuils devront être confrontés à des données réelles de terrain avant toute utilisation sur véhicule.
La plage de test du prototype est actuellement limitée à -50 °C à 200 °C. Cette plage est une règle de validation logicielle du prototype et ne constitue pas une plage de fonctionnement recommandée pour un véhicule.
3. Architecture logique actuelle
Entrée utilisateur
       │
       ├── Code DTC ───────► Base DTC ───────► Gravité + message
       │
       └── Température ────► Seuils indicatifs ─► Gravité + message
                                      │
                                      ▼
                           Historique JSON local
4. Validation et tests
Le projet contient des tests unitaires couvrant notamment :
DTC connu ;
DTC inconnu ;
normalisation d'un code DTC saisi avec espaces et minuscules ;
température normale ;
température en dérive ;
température élevée ;
températures aux seuils de décision ;
valeurs de température hors plage de test ;
entrée de température non numérique.
Exécution :
python -m unittest discover -s tests -v
La validation actuelle porte sur la logique logicielle du prototype. Elle ne constitue pas encore une validation sur véhicules réels.
5. Limites actuelles
Le prototype logiciel ne constitue pas encore le système AutoDiag complet.
Il ne réalise pas encore :
l'acquisition automatique depuis un boîtier OBD2 réel ;
la communication avec une application mobile ;
l'intégration de capteurs complémentaires ;
la validation statistique des seuils sur un jeu de données réel ;
un modèle prédictif entraîné sur des données de véhicules.
Ces limites sont volontairement documentées : elles définissent les prochaines étapes du projet.
6. Feuille de route
Étape 1 — Première expérience logicielle
Diagnostic DTC
Classification de gravité
Détection de température par seuils indicatifs
Historique JSON
Premiers tests unitaires
Validation des entrées et des limites du prototype
Étape 2 — Acquisition de données
Étudier et réaliser l'intégration d'un adaptateur OBD2 compatible
Acquérir des données réelles
Structurer les données de mesure
Étudier la qualité et la variabilité des mesures
Étape 3 — Détection d'anomalies
Construire un jeu de données
Étudier les tendances et séries temporelles
Comparer différentes approches de détection d'anomalies
Évaluer les performances sur des données séparées
Étape 4 — Système embarqué et application
Prototyper la chaîne d'acquisition embarquée
Intégrer des capteurs complémentaires, notamment la pression des pneus
Développer une interface mobile
Étudier des mécanismes d'alerte adaptés aux utilisateurs
7. Pourquoi ce projet évolue vers les systèmes embarqués
AutoDiag part d'un problème automobile concret et évolue vers une chaîne technique :
véhicule → acquisition de données → traitement → décision → alerte
La poursuite du projet nécessite progressivement des compétences en programmation, communication, acquisition de données, architecture matériel-logiciel et systèmes embarqués.
Cette trajectoire constitue le lien entre ma formation initiale en mécatronique et mon projet d'études en ingénierie des systèmes embarqués.
L'orientation vers les systèmes embarqués est cohérente avec la filière F1 de l'ISIMA, qui met notamment l'accent sur la conception et la programmation de systèmes embarqués et sur le couplage matériel/logiciel. AutoDiag constitue donc une première expérience personnelle que je souhaite approfondir par une formation d'ingénieur.
8. Statut
Projet personnel en cours de développement — première expérience v0.1.
Cette version est un prototype logiciel. Les évolutions matérielles, l'acquisition de données réelles et les approches avancées de détection d'anomalies restent à développer et à valider expérimentalement.
