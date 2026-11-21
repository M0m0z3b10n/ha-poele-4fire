"""Constantes pour l'intégration Poêle 4Fire."""

DOMAIN = "poele_4fire"
DEFAULT_NAME = "Poêle 4Heat (TiEmme) Wifi"
DEFAULT_HOST = "192.168.0.5"
DEFAULT_PORT = 80
SCAN_INTERVAL_SECONDS = 20

# Butées de température de consigne (sécurité logicielle Home Assistant)
MIN_TEMP = 10.0
MAX_TEMP = 25.0  # Bridage de sécurité à 25 °C (la carte mère accepte jusqu'à 40 °C)

CONF_HOST = "host"
CONF_PORT = "port"
CONF_NAME = "name"

# Table officielle des états TiEmme Elettronica / 4Fire
ETATS_POELE = {
    0: "Éteint",
    1: "Contrôle / Préchauffage",
    2: "Allumage (Chargement)",
    3: "Stabilisation (Flamme)",
    4: "Allumage (Flamme)",
    5: "En chauffe (Travail)",
    6: "Modulation",
    7: "Extinction en cours",
    8: "Sécurité",
    9: "Alarme / Blocage",
    10: "Récupération allumage",
    11: "Veille (Standby)",
}

# Codes d'erreur TiEmme Elettronica / 4Fire
# Format: code_int -> (libellé_court, description_complète, conseil_dépannage)
CODES_ERREURS = {
    0: (
        "Aucune erreur",
        "Le poêle fonctionne normalement.",
        "",
    ),
    1: (
        "Er01 — Thermostat de sécurité",
        "Le thermostat de sécurité thermique (Klixon) a déclenché. Surchauffe interne détectée.",
        "Laissez le poêle refroidir. Vérifiez que les grilles de ventilation ne sont pas obstruées et que le brasier est propre.",
    ),
    2: (
        "Er02 — Pressostat / Tirage",
        "Le pressostat de sécurité a détecté un défaut de tirage ou de dépression.",
        "Vérifiez que la porte du poêle est bien fermée, que le conduit de fumée n'est pas obstrué et que l'extracteur tourne normalement.",
    ),
    3: (
        "Er03 — Extinction (manque de chaleur)",
        "Le poêle s'est éteint car la température des fumées est trop basse. Manque de granulés probable.",
        "Vérifiez le niveau du réservoir. Si plein, réamorcez la vis sans fin ou nettoyez le brûleur.",
    ),
    4: (
        "Er04 — Défaut sonde de température",
        "La sonde de température ambiante ou de l'échangeur est défectueuse (coupure ou court-circuit).",
        "Vérifiez le connecteur de la sonde. Si le problème persiste, remplacez la sonde.",
    ),
    5: (
        "Er05 — Surchauffe des fumées",
        "La température des fumées a dépassé le seuil maximum de sécurité.",
        "Vérifiez que le conduit n'est pas partiellement obstrué. Nettoyez l'échangeur et le conduit.",
    ),
    6: (
        "Er06 — Défaut sonde fumées",
        "La sonde de température des fumées est en défaut (coupure ou court-circuit).",
        "Vérifiez le câblage de la sonde de fumées. Si la sonde est endommagée, remplacez-la.",
    ),
    7: (
        "Er07 — Défaut sonde eau / échangeur",
        "La sonde de température du circuit hydraulique est défectueuse.",
        "Vérifiez le branchement de la sonde eau. Remplacez si nécessaire.",
    ),
    8: (
        "Er08 — Défaut coupure secteur",
        "Une coupure de courant a eu lieu pendant que le poêle était en fonctionnement.",
        "Aucune action requise. Le poêle redémarre automatiquement si programmé.",
    ),
    9: (
        "Er09 — Blocage de la vis sans fin",
        "La vis d'alimentation en granulés est bloquée ou surchargée.",
        "Vérifiez qu'il n'y a pas de granulés compactés ou un corps étranger dans la vis. Nettoyez et testez le moteur.",
    ),
    12: (
        "Er12 — Échec d'allumage",
        "La flamme n'a pas pris dans le délai imparti lors de la phase d'allumage.",
        "Vérifiez que le brasier est propre, que la résistance d'allumage fonctionne et que les granulés tombent bien dans le brûleur.",
    ),
    13: (
        "Er13 — Extinction flamme en fonctionnement",
        "La flamme s'est éteinte de façon inattendue en cours de chauffe.",
        "Vérifiez le niveau des granulés, l'état du brûleur et le tirage de la cheminée.",
    ),
    14: (
        "Er14 — Surchauffe carte électronique",
        "La température de la carte mère a dépassé le seuil de sécurité.",
        "Vérifiez la ventilation du boîtier électronique. Contactez un technicien si l'erreur persiste.",
    ),
    15: (
        "Er15 — Coupure secteur en chauffe",
        "Une micro-coupure de courant a été détectée pendant la phase de chauffe.",
        "Vérifiez la stabilité de votre alimentation secteur. L'onduleur peut être une solution.",
    ),
}

# Nombre maximal d'entrées conservées dans l'historique des erreurs
MAX_HISTORIQUE_ERREURS = 10
