"""
AutoDiag — Moteur de diagnostic prédictif automobile low-cost
Auteure : Evouna Sonia Ninon

Ce script simule le cœur logique du système AutoDiag : à partir d'un code
défaut (DTC) lu sur la prise OBD2 d'un véhicule, il détermine un niveau de
gravité (Vert / Orange / Rouge) et génère un message clair, compréhensible
par un conducteur non technicien — y compris une version "alerte vocale"
en langage courant.

Les codes DTC utilisés ici sont des codes génériques standardisés
(norme SAE J2012 / ISO 15031-6), utilisés par tous les véhicules
compatibles OBD2 dans le monde.
"""

import json
import os
from datetime import datetime

# --- Base de données des codes DTC les plus courants ---
# Format : code -> (description technique, gravité)
# Gravité : "VERT" (surveillance), "ORANGE" (à traiter prochainement),
# "ROUGE" (urgent, risque pour le véhicule ou la sécurité)

DTC_DATABASE = {
    "P0100": ("Circuit du débitmètre d'air défaillant", "ORANGE"),
    "P0115": ("Circuit de température du liquide de refroidissement défaillant", "ORANGE"),
    "P0128": ("Thermostat : température de refroidissement sous le seuil attendu", "ORANGE"),
    "P0171": ("Mélange air/carburant trop pauvre (Banc 1)", "ORANGE"),
    "P0174": ("Mélange air/carburant trop pauvre (Banc 2)", "ORANGE"),
    "P0217": ("Surchauffe moteur détectée", "ROUGE"),
    "P0230": ("Circuit primaire de la pompe à carburant défaillant", "ROUGE"),
    "P0300": ("Ratés d'allumage aléatoires détectés sur plusieurs cylindres", "ROUGE"),
    "P0301": ("Raté d'allumage détecté sur le cylindre 1", "ORANGE"),
    "P0325": ("Circuit du capteur de cliquetis défaillant", "ORANGE"),
    "P0420": ("Efficacité du catalyseur sous le seuil attendu (Banc 1)", "VERT"),
    "P0440": ("Anomalie dans le système de contrôle des vapeurs d'essence (EVAP)", "VERT"),
    "P0500": ("Circuit du capteur de vitesse véhicule défaillant", "ORANGE"),
    "P0562": ("Tension système anormalement basse", "ROUGE"),
    "P0601": ("Erreur de mémoire interne du calculateur moteur", "ORANGE"),
    "P0700": ("Anomalie détectée dans le système de transmission", "ORANGE"),
}

# Messages clairs associés à chaque niveau de gravité, pour l'alerte vocale
MESSAGES_GRAVITE = {
    "VERT": "Anomalie mineure détectée. Aucune action urgente n'est nécessaire, mais surveillez votre véhicule.",
    "ORANGE": "Anomalie détectée. Il est recommandé de faire vérifier votre véhicule prochainement.",
    "ROUGE": "Anomalie sérieuse détectée. Arrêtez-vous dès que possible et faites vérifier votre véhicule.",
}

HISTORIQUE_FICHIER = "historique_diagnostics.json"


def diagnostiquer(code_dtc: str) -> dict:
    """
    Prend un code DTC en entrée et retourne un diagnostic complet :
    description technique, niveau de gravité, et message clair pour
    le conducteur (base de l'alerte vocale).
    """
    code_dtc = code_dtc.strip().upper()

    if code_dtc not in DTC_DATABASE:
        return {
            "code": code_dtc,
            "description": "Code non reconnu dans la base AutoDiag actuelle.",
            "gravite": "INCONNU",
            "message": "Ce code n'est pas encore reconnu par AutoDiag. Consultez un garagiste.",
        }

    description, gravite = DTC_DATABASE[code_dtc]
    return {
        "code": code_dtc,
        "description": description,
        "gravite": gravite,
        "message": MESSAGES_GRAVITE[gravite],
    }


def evaluer_temperature_moteur(temperature_celsius: float) -> dict:
    """
    Évaluation PRÉDICTIVE (et non réactive) : à partir d'une lecture de
    température moteur en direct, détecte une dérive AVANT qu'un code
    défaut comme P0217 (surchauffe) ne soit déclenché par le véhicule.

    C'est la différence entre diagnostic réactif (lire un code après coup)
    et diagnostic prédictif (anticiper avant l'apparition du code) —
    l'objectif central d'AutoDiag.

    Seuils indicatifs (à affiner avec des données réelles de terrain) :
    - < 95°C  : normal
    - 95-104°C : dérive à surveiller
    - >= 105°C : risque de surchauffe imminent
    """
    if temperature_celsius >= 105:
        gravite = "ROUGE"
        message = (
            f"Température moteur anormalement élevée ({temperature_celsius}°C). "
            "Arrêtez-vous dès que possible, avant qu'un code défaut ne soit déclenché."
        )
    elif temperature_celsius >= 95:
        gravite = "ORANGE"
        message = (
            f"Température moteur en légère dérive ({temperature_celsius}°C). "
            "Surveillez et faites vérifier le circuit de refroidissement prochainement."
        )
    else:
        gravite = "VERT"
        message = f"Température moteur normale ({temperature_celsius}°C)."

    return {
        "type": "lecture_predictive",
        "parametre": "température moteur",
        "valeur": temperature_celsius,
        "gravite": gravite,
        "message": message,
    }


def enregistrer_historique(diagnostic: dict):
    """Enregistre chaque diagnostic effectué dans un historique JSON local."""
    historique = []
    if os.path.exists(HISTORIQUE_FICHIER):
        with open(HISTORIQUE_FICHIER, "r", encoding="utf-8") as f:
            historique = json.load(f)

    diagnostic_horodate = dict(diagnostic)
    diagnostic_horodate["date"] = datetime.now().isoformat(timespec="seconds")
    historique.append(diagnostic_horodate)

    with open(HISTORIQUE_FICHIER, "w", encoding="utf-8") as f:
        json.dump(historique, f, ensure_ascii=False, indent=2)


def afficher_diagnostic(diagnostic: dict):
    """Affiche le diagnostic dans le terminal avec un code couleur simple."""
    couleurs_ansi = {"VERT": "\033[92m", "ORANGE": "\033[93m", "ROUGE": "\033[91m", "INCONNU": "\033[90m"}
    reset = "\033[0m"
    couleur = couleurs_ansi.get(diagnostic["gravite"], "")

    print(f"\nCode : {diagnostic['code']}")
    print(f"Description : {diagnostic['description']}")
    print(f"Gravité : {couleur}{diagnostic['gravite']}{reset}")
    print(f"Alerte vocale (texte) : \"{diagnostic['message']}\"\n")


def afficher_lecture_predictive(lecture: dict):
    """Affiche une lecture prédictive (ex. température) avec code couleur."""
    couleurs_ansi = {"VERT": "\033[92m", "ORANGE": "\033[93m", "ROUGE": "\033[91m"}
    reset = "\033[0m"
    couleur = couleurs_ansi.get(lecture["gravite"], "")

    print(f"\nParamètre surveillé : {lecture['parametre']} = {lecture['valeur']}°C")
    print(f"Gravité : {couleur}{lecture['gravite']}{reset}")
    print(f"Alerte vocale (texte) : \"{lecture['message']}\"\n")


if __name__ == "__main__":
    print("=== AutoDiag — Simulateur de diagnostic prédictif (v0.2) ===")
    print("1 = Diagnostiquer à partir d'un code DTC (réactif)")
    print("2 = Lecture prédictive de la température moteur (avant panne)")
    print("q = Quitter\n")

    while True:
        mode = input("Mode (1/2/q) > ").strip().lower()
        if mode in ("q", "quitter", "exit"):
            break
        elif mode == "1":
            entree = input("Code DTC > ")
            diagnostic = diagnostiquer(entree)
            afficher_diagnostic(diagnostic)
            enregistrer_historique(diagnostic)
        elif mode == "2":
            try:
                temp = float(input("Température moteur (°C) > "))
            except ValueError:
                print("Merci d'entrer un nombre valide.\n")
                continue
            lecture = evaluer_temperature_moteur(temp)
            afficher_lecture_predictive(lecture)
            enregistrer_historique(lecture)
        else:
            print("Choix non reconnu.\n")

    print("Historique enregistré dans", HISTORIQUE_FICHIER)
