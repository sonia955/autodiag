"""
AutoDiag v0.1 — Prototype logiciel de diagnostic automobile.

Projet personnel d'Evouna Sonia Ninon.
Le prototype explore deux approches :
- diagnostic réactif à partir de codes DTC ;
- détection précoce d'une anomalie de température par seuils indicatifs.

Les seuils de température ne constituent pas un modèle prédictif validé :
ils devront être confrontés à des données réelles de terrain.
"""

import json
import os
from datetime import datetime


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


MESSAGES_GRAVITE = {
    "VERT": "Anomalie mineure détectée. Aucune action urgente n'est nécessaire, mais surveillez votre véhicule.",
    "ORANGE": "Anomalie détectée. Il est recommandé de faire vérifier votre véhicule prochainement.",
    "ROUGE": "Anomalie sérieuse détectée. Faites vérifier le véhicule rapidement et évitez de poursuivre si la situation est dangereuse.",
}


HISTORIQUE_FICHIER = "historique_diagnostics.json"


def diagnostiquer(code_dtc: str) -> dict:
    """Analyse un code DTC et retourne un diagnostic structuré."""
    code_dtc = code_dtc.strip().upper()

    if code_dtc not in DTC_DATABASE:
        return {
            "type": "diagnostic_dtc",
            "code": code_dtc,
            "description": "Code non reconnu dans la base AutoDiag actuelle.",
            "gravite": "INCONNU",
            "message": "Ce code n'est pas encore reconnu par AutoDiag. Consultez un garagiste.",
        }

    description, gravite = DTC_DATABASE[code_dtc]
    return {
        "type": "diagnostic_dtc",
        "code": code_dtc,
        "description": description,
        "gravite": gravite,
        "message": MESSAGES_GRAVITE[gravite],
    }


def evaluer_temperature_moteur(temperature_celsius: float) -> dict:
    """
    Détecte une dérive de température à partir de seuils indicatifs.

    Cette fonction est une première approche de détection précoce d'anomalie,
    et non un modèle prédictif validé. Les seuils devront être affinés à
    partir de données réelles de terrain.
    """
    if not isinstance(temperature_celsius, (int, float)):
        raise ValueError("La température doit être une valeur numérique.")

    if temperature_celsius < -50 or temperature_celsius > 200:
        raise ValueError("Température hors de la plage de test du prototype (-50 à 200 °C).")

    if temperature_celsius >= 105:
        gravite = "ROUGE"
        message = (
            f"Température moteur élevée ({temperature_celsius}°C). "
            "Faites vérifier le véhicule et évitez de poursuivre si la situation est dangereuse."
        )
    elif temperature_celsius >= 95:
        gravite = "ORANGE"
        message = (
            f"Température moteur en dérive ({temperature_celsius}°C). "
            "Surveillez le véhicule et faites vérifier le circuit de refroidissement."
        )
    else:
        gravite = "VERT"
        message = f"Température moteur dans la plage normale du prototype ({temperature_celsius}°C)."

    return {
        "type": "lecture_temperature",
        "parametre": "température moteur",
        "valeur": temperature_celsius,
        "gravite": gravite,
        "message": message,
    }


def enregistrer_historique(diagnostic: dict) -> None:
    """Enregistre un diagnostic dans un historique JSON local."""
    historique = []

    if os.path.exists(HISTORIQUE_FICHIER):
        try:
            with open(HISTORIQUE_FICHIER, "r", encoding="utf-8") as fichier:
                historique = json.load(fichier)
        except (json.JSONDecodeError, OSError):
            historique = []

    diagnostic_horodate = dict(diagnostic)
    diagnostic_horodate["date"] = datetime.now().isoformat(timespec="seconds")
    historique.append(diagnostic_horodate)

    with open(HISTORIQUE_FICHIER, "w", encoding="utf-8") as fichier:
        json.dump(historique, fichier, ensure_ascii=False, indent=2)


def afficher_diagnostic(diagnostic: dict) -> None:
    """Affiche un diagnostic DTC dans le terminal."""
    couleurs_ansi = {
        "VERT": "\033[92m",
        "ORANGE": "\033[93m",
        "ROUGE": "\033[91m",
        "INCONNU": "\033[90m",
    }
    reset = "\033[0m"
    couleur = couleurs_ansi.get(diagnostic["gravite"], "")

    print(f"\nCode : {diagnostic['code']}")
    print(f"Description : {diagnostic['description']}")
    print(f"Gravité : {couleur}{diagnostic['gravite']}{reset}")
    print(f"Message utilisateur : \"{diagnostic['message']}\"\n")


def afficher_lecture_temperature(lecture: dict) -> None:
    """Affiche une lecture de température dans le terminal."""
    couleurs_ansi = {"VERT": "\033[92m", "ORANGE": "\033[93m", "ROUGE": "\033[91m"}
    reset = "\033[0m"
    couleur = couleurs_ansi.get(lecture["gravite"], "")

    print(f"\nParamètre surveillé : {lecture['parametre']} = {lecture['valeur']}°C")
    print(f"Gravité : {couleur}{lecture['gravite']}{reset}")
    print(f"Message utilisateur : \"{lecture['message']}\"\n")


def main() -> None:
    print("=== AutoDiag v0.1 — Prototype logiciel de diagnostic automobile ===")
    print("1 = Diagnostic à partir d'un code DTC (réactif)")
    print("2 = Détection précoce d'anomalie de température (seuils indicatifs)")
    print("q = Quitter\n")

    while True:
        mode = input("Mode (1/2/q) > ").strip().lower()

        if mode in ("q", "quitter", "exit"):
            break

        if mode == "1":
            entree = input("Code DTC > ")
            diagnostic = diagnostiquer(entree)
            afficher_diagnostic(diagnostic)
            enregistrer_historique(diagnostic)

        elif mode == "2":
            try:
                temperature = float(input("Température moteur (°C) > "))
                lecture = evaluer_temperature_moteur(temperature)
            except ValueError as erreur:
                print(f"Entrée invalide : {erreur}\n")
                continue

            afficher_lecture_temperature(lecture)
            enregistrer_historique(lecture)

        else:
            print("Choix non reconnu.\n")

    print("Historique enregistré dans", HISTORIQUE_FICHIER)


if __name__ == "__main__":
    main()
