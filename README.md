# Integration Home Assistant - Poele 4Fire / HottoH (TiEmme)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=M0m0z3b10n&repository=ha-poele-4fire&category=integration)

Composant personnalise pour piloter en local via Wi-Fi les poeles a granules 4Fire et equipements bases sur l'electronique TiEmme Elettronica (cartes SY250 / protocoles 2WL et 2WC sur le port TCP 80) piloté par l'application 4Heat.

## Fonctionnalites

- **Entite Climate (`climate.poele_4fire`)** :
  - Reglage precis de la temperature de consigne au dixieme de degre (ex: 21.5 °C).
  - Affichage en direct de la temperature ambiante mesuree par la sonde.
  - Modes HVAC : `off` (Eteint) et `heat` (Allume / En chauffe).
  - Actions detaillees : `preheating` (Controle, Chargement, Flamme), `heating` (Travail, Modulation), `off` (Eteint).
  - Support complet des cartes Lovelace et de la carte **Scheduler** (`supported_features: 385`).

- **Capteurs dedies (`sensor`)** :
  - Temperature des fumees (°C)
  - Puissance active (ex: P1 a P5)
  - Etat detaille (Prechauffage, Allumage, Modulation, etc.)
  - Horloge interne du poele

## Installation

### Option 1 : Via HACS (Recommande)

#### Installation en un clic :
Cliquez simplement sur ce bouton pour ouvrir directement le dépôt dans votre HACS :

[![Ajouter le dépôt à HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=M0m0z3b10n&repository=ha-poele-4fire&category=integration)

#### Installation manuelle dans HACS :
1. Ouvrez **HACS** dans votre Home Assistant.
2. Cliquez sur les 3 points en haut à droite > **Dépôts personnalisés**.
3. Ajoutez l'URL : `https://github.com/M0m0z3b10n/ha-poele-4fire` avec la catégorie **Intégration**.
4. Cliquez sur **Télécharger**, puis redémarrez Home Assistant.

### Option 2 : Installation manuelle

Copiez le dossier `custom_components/poele_4fire` dans le repertoire `config/custom_components/` de votre serveur Home Assistant, puis redemarrez Home Assistant.

## Configuration

Rendez-vous dans **Parametres** > **Appareils et services** > **Ajouter une integration** :
1. Recherchez **Poele 4Fire**.
2. Indiquez l'adresse IP locale de votre poele (ex: `192.168.0.5`) et le port (`80`).
3. Validez : l'appareil et l'ensemble de ses entites sont crees automatiquement.

## Licence

Distribué sous licence MIT.
