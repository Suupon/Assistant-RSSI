# 🛡️Assistant RSSI Virtuel

Assistant RSSI Virtuel est une application web interactive basée sur Streamlit et Ollama pour répondre à toutes vos questions liées à la cybersécurité, synthétiser des documents PDF, faire de la veille CERT-FR, gérer une FAQ et enrichir votre base documentaire interne.

---

## 🚀 Fonctionnalités principales

* **Assistant intelligent** : Dialogue en langage naturel sur la cybersécurité, basé sur vos documents internes (RAG) et un modèle LLM local.
* **Synthèse de documents PDF** : Résumés automatiques de rapports ou bulletins techniques.
* **Veille CERT-FR** : Intégration des flux RSS officiels avec résumé automatique.
* **Historique des échanges** : Sauvegarde automatique dans un fichier `.jsonl`.
* **Ajout de documents** : Glissez vos PDF dans `docs/` pour enrichir la base documentaire.
* **Interface légère** : Accessible depuis un navigateur local via Streamlit.

---

## 🐳 Installation via Docker

### ⚙️ Prérequis

* Docker installé sur votre machine
* Modèle Ollama compatible (ex : `mistral`) téléchargé automatiquement

### 📂 Arborescence simplifiée du projet

```
/ (racine)
├── rssi.py                 # Interface Streamlit (frontend)
├── backend/                # Fonctions métier
│   ├── pdf_utils.py
│   ├── faiss_utils.py
│   ├── llm_utils.py
│   ├── rss_utils.py
│   └── history_utils.py
├── docs/                   # PDF internes à indexer
├── conversations.jsonl     # Historique de l'assistant
├── requirements.txt        # Dépendances Python
├── start.sh                # Script de lancement (Ollama + Streamlit)
├── Dockerfile              # Image Docker complète
└── README.md               # Ce fichier
```

### ▶️ Démarrage (une seule commande)

```bash
docker build -t assistant-rssi .
docker run -p 8501:8501 assistant-rssi
```

> 💡 Le script `start.sh` lance automatiquement `ollama serve`, charge le modèle `mistral`, puis démarre l'application Streamlit.

L'application sera accessible à l’adresse : [http://localhost:8501](http://localhost:8501)

---

## 🔧 Si vous utilisez sans Docker (optionnel)

### ⚙️ Prérequis

* Python 3.8+
* [Ollama](https://ollama.com/) installé manuellement sur votre machine

### ▶️ Installation manuelle

```bash
pip install -r requirements.txt
ollama serve &
ollama run mistral &
streamlit run rssi.py
```

---

## 📦 Dépendances principales

* `streamlit`
* `requests`
* `PyMuPDF`
* `sentence-transformers`
* `faiss-cpu`
* `feedparser`

---

## 🧐 Conseils

* Placez vos fichiers PDF dans `docs/` pour que l’assistant les prenne en compte.
* L’historique de chaque échange est stocké dans `conversations.jsonl`.
* L’ouverture du navigateur n’est pas automatique dans Docker, mais vous pouvez le faire manuellement : `open http://localhost:8501` sur Mac.

---

## 📄 Licence

Projet éducatif et démonstratif. À adapter selon vos besoins professionnels.
