"""Constantes pour l'intégration Poêle 4Fire."""

DOMAIN = "poele_4fire"
DEFAULT_NAME = "Poêle 4Fire"
DEFAULT_HOST = "192.168.0.5"
DEFAULT_PORT = 80
SCAN_INTERVAL_SECONDS = 20

CONF_HOST = "host"
CONF_PORT = "port"
CONF_NAME = "name"

# Table officielle des états TiEmme Elettronica / 4Fire
ETATS_POELE = {
    0: "Éteint",
    1: "Contrôle / Préchauffage",
    2: "Allumage (Chargement)",
    3: "Stabilisation (Flamme)",
    4: "En chauffe (Travail)",
    5: "Extinction en cours",
    6: "Modulation",
    7: "Veille (Stand-by)",
    8: "Alarme / Sécurité",
}
