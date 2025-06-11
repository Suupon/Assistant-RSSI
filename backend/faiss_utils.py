"""
Module faiss_utils.py
Fonctions utilitaires pour l'encodage, l'indexation et la recherche vectorielle avec FAISS.
"""
import faiss

def construire_index(model, chunks):
    """
    Encode les chunks en vecteurs et construit un index FAISS.
    Args:
        model: Modèle d'embedding SentenceTransformer.
        chunks (list): Liste de textes à indexer.
    Returns:
        (faiss.Index, np.ndarray): L'index FAISS et les vecteurs encodés.
    """
    vecteurs = model.encode(chunks)
    index = faiss.IndexFlatL2(vecteurs.shape[1])
    index.add(vecteurs)
    return index, vecteurs

def rechercher_passages(model, question, chunks, index, top_k=3):
    """
    Recherche les passages les plus proches d'une question dans l'index FAISS.
    Args:
        model: Modèle d'embedding SentenceTransformer.
        question (str): Question utilisateur.
        chunks (list): Liste des chunks indexés.
        index (faiss.Index): Index FAISS.
        top_k (int): Nombre de passages à retourner.
    Returns:
        list: Passages les plus pertinents.
    """
    vecteur_question = model.encode([question])
    distances, indices = index.search(vecteur_question, top_k)
    passages = [chunks[i] for i in indices[0]]
    return passages 