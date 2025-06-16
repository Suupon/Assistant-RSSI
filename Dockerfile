FROM python:3.11-slim

# Installer les outils système nécessaires à la compilation, à curl et à netcat
RUN apt-get update && \
    apt-get install -y build-essential curl netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Installer Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Définir le répertoire de travail
WORKDIR /app

# Copier tous les fichiers
COPY . .

# Installer les dépendances Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Rendre le script exécutable
RUN chmod +x start.sh

# Exposer le port de Streamlit
EXPOSE 8501

# Commande de lancement
CMD ["./start.sh"]
