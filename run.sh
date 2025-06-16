#!/bin/bash

# Lancer le conteneur Docker
docker run -d -p 8501:8501 rssi

# Attendre quelques secondes que Streamlit démarre
sleep 3

# Ouvrir automatiquement le navigateur
open http://localhost:8501

