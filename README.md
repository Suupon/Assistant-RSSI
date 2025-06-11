# 🛡️ Assistant RSSI Virtuel

Assistant RSSI Virtuel est une application web interactive pour répondre à toutes vos questions liées à la cybersécurité, synthétiser des documents PDF, faire de la veille CERT-FR, gérer une FAQ et enrichir votre base documentaire interne.

## Fonctionnalités principales
- **Assistant intelligent** : Posez des questions sur la cybersécurité, les normes, les incidents, etc. L'assistant s'appuie sur vos documents PDF internes (RAG) et ses connaissances générales.
- **Synthèse de documents** : Téléversez un PDF (rapport, guide, bulletin...) et obtenez un résumé clair et structuré.
- **Veille CERT-FR** : Consultez les dernières alertes du CERT-FR et obtenez un résumé automatique de chaque alerte.
- **FAQ cybersécurité** : Accédez à une liste de questions fréquentes et obtenez des réponses instantanées.
- **Ajout de documents** : Ajoutez facilement vos propres PDF à la base documentaire.
- **Historique** : Retrouvez tous vos échanges et exportez-les en JSON.

## Installation

### Prérequis
- Python 3.8+
- [Ollama](https://ollama.com/) (pour le LLM local, ex : mistral)

### Installation des dépendances
```bash
pip install -r requirements.txt
```

### Lancement du serveur LLM (Ollama)
Assurez-vous qu'Ollama est installé et lancé sur votre machine :
```bash
ollama serve
ollama run mistral
```

### Lancement de l'application
```bash
streamlit run app.py
```

L'application sera accessible sur [http://localhost:8501](http://localhost:8501)

## Structure du projet
```
/ (racine)
│
├── app.py                  # Interface Streamlit (front-end)
├── backend/                # Fonctions métier et utilitaires
│   ├── pdf_utils.py        # Lecture et découpage des PDF
│   ├── faiss_utils.py      # Indexation et recherche vectorielle
│   ├── llm_utils.py        # Appel au LLM (Ollama)
│   ├── rss_utils.py        # Récupération des alertes CERT-FR
│   └── history_utils.py    # Gestion de l'historique
│
├── docs/                   # Dossier pour vos PDF internes
├── conversations.jsonl     # Historique des échanges
├── requirements.txt        # Dépendances Python
└── README.md               # Ce fichier
```

## Conseils d'utilisation
- Ajoutez vos documents PDF dans le dossier `docs/` pour enrichir les réponses de l'assistant.
- Si aucun document n'est présent, l'assistant répondra uniquement avec ses connaissances générales.
- L'historique est sauvegardé automatiquement et exportable.

## Dépendances principales
- streamlit
- requests
- PyMuPDF
- sentence-transformers
- faiss-cpu
- feedparser

## Licence
Projet éducatif et démonstratif. À adapter selon vos besoins professionnels. 