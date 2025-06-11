"""
Module pdf_utils.py
Fonctions utilitaires pour lire et découper les fichiers PDF en chunks exploitables pour le RAG.
"""
import os
import fitz
import streamlit as st

def lire_et_chunker_pdfs(dossier="docs", taille_chunk=500, chevauchement=100):
    """
    Lit tous les fichiers PDF d'un dossier, extrait le texte et le découpe en petits morceaux (chunks).
    Args:
        dossier (str): Dossier contenant les PDF.
        taille_chunk (int): Taille d'un chunk de texte.
        chevauchement (int): Nombre de caractères de recouvrement entre deux chunks.
    Returns:
        (list, list): Liste des chunks, liste des fichiers d'origine pour chaque chunk.
    """
    chunks = []
    metadatas = []
    for fichier in os.listdir(dossier):
        if fichier.lower().endswith(".pdf"):
            chemin = os.path.join(dossier, fichier)
            try:
                doc = fitz.open(chemin)
                texte = ""
                for page in doc:
                    texte += page.get_text()
                # Découpage du texte en chunks
                for i in range(0, len(texte), taille_chunk - chevauchement):
                    chunk = texte[i:i + taille_chunk]
                    if len(chunk.strip()) > 0:
                        chunks.append(chunk)
                        metadatas.append(fichier)
            except Exception as e:
                st.warning(f"Erreur de lecture de {fichier} : {e}")
    return chunks, metadatas 