"""
Module llm_utils.py
Fonctions utilitaires pour l'appel au LLM local (Ollama).
"""
import requests

def generer_reponse_llm(prompt, model_name="mistral"):
    """
    Envoie un prompt au LLM local via l'API Ollama et récupère la réponse générée.
    Args:
        prompt (str): Prompt à envoyer au modèle.
        model_name (str): Nom du modèle à utiliser.
    Returns:
        str: Réponse générée par le LLM.
    """
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model_name,
        "prompt": prompt,
        "stream": False
    })
    return response.json().get("response", "❌ Pas de réponse générée.") 