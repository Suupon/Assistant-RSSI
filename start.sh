#!/bin/bash

# Lancer le serveur Ollama en arrière-plan
ollama serve &

# Attendre que le port 11434 réponde (Ollama écoute dessus)
echo "⌛ Attente que le serveur Ollama soit prêt..."
while ! nc -z localhost 11434; do   
  sleep 1
done
echo "✅ Serveur Ollama prêt."

# Charger le modèle mistral sans interaction
ollama run mistral < /dev/null &

# Lancer Streamlit
streamlit run rssi.py

