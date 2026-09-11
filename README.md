# AutoDiag — Diagnostic prédictif automobile low-cost

`Prototype fonctionnel v0.1` · `Python` · `OBD2`

**Auteure :** Evouna Sonia Ninon
**Contexte :** Projet personnel, développé en autoformation (Python), dans le cadre d'une candidature à la Bourse d'Excellence Eiffel (Cycle Ingénieur, filière F1 — ISIMA).

## Le projet

AutoDiag est un projet de diagnostic prédictif automobile low-cost, pensé d'abord pour les chauffeurs de taxi de Yaoundé (Cameroun), pour qui l'entretien préventif reste souvent un arbitrage financier difficile.

Le concept complet repose sur :
1. Un **boîtier connecté à la prise OBD2** du véhicule, qui collecte en continu les données moteur.
2. Une **application mobile** qui interprète ces données pour anticiper l'apparition d'une panne, via un code de gravité simple (🟢 Vert / 🟠 Orange / 🔴 Rouge).
3. Pour les véhicules haut de gamme, une **alerte vocale** en langage clair.

## Ce dépôt

Ce dépôt contient une **première version fonctionnelle du moteur de diagnostic** (`autodiag.py`), avec deux modes :

1. **Mode réactif** : à partir d'un code défaut (DTC) lu sur la prise OBD2, retourne une description technique, un niveau de gravité (Vert / Orange / Rouge) et un message clair, à la base de la future alerte vocale.
2. **Mode prédictif** : à partir d'une lecture en direct d'un paramètre moteur (ex. température), détecte une dérive anormale **avant** qu'un code défaut ne soit déclenché par le véhicule — c'est la différence entre un diagnostic réactif (constater après coup) et un diagnostic réellement prédictif (anticiper), qui est l'ambition centrale d'AutoDiag.

Les codes DTC utilisés sont des codes génériques réels, standardisés par la norme SAE J2012 / ISO 15031-6, communs à tous les véhicules compatibles OBD2. Les seuils de température utilisés dans le mode prédictif sont indicatifs et seront affinés avec des données réelles de terrain.

Un historique des diagnostics et lectures effectués est automatiquement enregistré (`historique_diagnostics.json`).

## Utilisation

```bash
python3 autodiag.py
```

Choisissez ensuite le mode 1 (code DTC) ou 2 (lecture prédictive de température), et entrez la valeur demandée.

## Vision — évolutions futures

- **Intégration matérielle réelle** avec un boîtier OBD2 Bluetooth (tests en cours sur véhicules réels).
- **Élargissement de la base de codes DTC** et des paramètres surveillés en mode prédictif (au-delà de la température).
- **Intégration de capteurs complémentaires** (pression des pneus), au-delà de ce que couvre l'OBD2 seul.
- **Accessibilité sans smartphone** : de nombreux chauffeurs de taxi à Yaoundé n'ont pas de smartphone. Une évolution envisagée consiste à adapter le niveau d'alerte au canal disponible : pas de notification pour un niveau Vert, un SMS quotidien pour un niveau Orange, un appel vocal automatique pour un niveau Rouge.
- **Diagnostic à seuils prédictifs plus larges**, dans une logique proche des approches de maintenance prédictive étudiées en recherche (réseaux de capteurs, systèmes embarqués).
- Développement de l'application mobile (interface, alerte vocale audio).

## Statut

Projet en cours de conception active. Cette version est un prototype logiciel du moteur de diagnostic, pas encore du produit final.

Ce prototype constitue la base technique de mon projet professionnel déposé pour la Bourse d'Excellence Eiffel — Cycle Ingénieur ISIMA, filière F1.
