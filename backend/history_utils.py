"""
Module history_utils.py
Fonctions utilitaires pour la gestion de l'historique des conversations (sauvegarde et chargement).
"""
import os
import json
from datetime import datetime

def sauvegarder_echange(question, reponse, fichier="conversations.jsonl"):
    """
    Sauvegarde un échange question/réponse dans un fichier JSONL.
    Args:
        question (str): Question posée.
        reponse (str): Réponse générée.
        fichier (str): Fichier de sauvegarde.
    """
    echange = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "reponse": reponse
    }
    with open(fichier, "a", encoding="utf-8") as f:
        f.write(json.dumps(echange, ensure_ascii=False) + "\n")

def charger_historique_persistant(fichier="conversations.jsonl"):
    """
    Charge l'historique des conversations depuis un fichier JSONL.
    Args:
        fichier (str): Fichier d'historique.
    Returns:
        list: Liste des échanges question/réponse.
    """
    if not os.path.exists(fichier):
        return []
    historique = []
    with open(fichier, "r", encoding="utf-8") as f:
        for ligne in f:
            try:
                e = json.loads(ligne)
                historique.append({"question": e["question"], "reponse": e["reponse"]})
            except:
                continue
    return historique 