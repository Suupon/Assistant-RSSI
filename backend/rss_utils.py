"""
Module rss_utils.py
Fonctions utilitaires pour la récupération et le parsing des alertes RSS CERT-FR.
"""
import feedparser
import urllib.request

def get_alertes_certfr():
    """
    Récupère les dernières alertes du flux RSS CERT-FR.
    Returns:
        list: Liste de dictionnaires contenant titre, date, description et lien de chaque alerte.
    """
    flux_url = "https://www.cert.ssi.gouv.fr/feed/"
    req = urllib.request.Request(
        flux_url,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req) as response:
        xml = response.read()
    feed = feedparser.parse(xml)
    articles_tries = sorted(
        feed.entries,
        key=lambda entry: entry.published_parsed,
        reverse=True
    )
    alertes = []
    for entry in articles_tries[:5]:
        alertes.append({
            "titre": entry.title,
            "date": entry.published,
            "description": entry.summary,
            "lien": entry.link
        })
    return alertes 