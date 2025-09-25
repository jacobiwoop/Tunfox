# TunFox - Client Tunnel

Un client Python pour créer des tunnels sécurisés et exposer vos services locaux sur Internet via des sous-domaines publics.

## 🚀 Fonctionnalités

- **Exposition simple** : Rendez vos services locaux accessibles depuis Internet
- **Sous-domaines automatiques** : Génération automatique ou personnalisation des noms de tunnel
- **Reconnexion automatique** : Gestion intelligente des déconnexions
- **Mode verbose** : Logs détaillés pour le débogage
- **Configuration flexible** : Paramètres personnalisables via arguments

## 🛠 Installation

### 📦 Récupération du code
```bash
git clone https://github.com/jacobiwoop/Tunfox.git
cd Tunfox
```

### 🐍 Installation Python (si nécessaire)
```bash
# Installation des dépendances
pip install -r requirements.txt

# Ou installation manuelle
pip install websockets requests
```

### ⚡ Installation de l'exécutable  
```bash
# Rendre l'exécutable utilisable
chmod +x tunfox

# Installation globale (nécessite sudo/admin)
sudo cp tunfox /usr/local/bin/

# Vérification
tunfox --help
```

### 🏠 Installation locale 
```bash
# Copie dans le dossier personnel
mkdir -p ~/.local/bin
cp tunfox ~/.local/bin/

# Ajout au PATH (ajouter à ~/.bashrc ou ~/.zshrc)
export PATH="$HOME/.local/bin:$PATH"

# Rechargement du shell
source ~/.bashrc  # ou source ~/.zshrc
```

### 📁 Structure du projet

Après clonage, vous trouverez :
```
Tunfox/
├── tunfox              # Exécutable binaire  
├── tunfox.py          # Script Python 
├── requirements.txt   # Dépendances Python
└── README.md         # Documentation
```

## 🚀 Démarrage rapide

1. **Installation express** :
   ```bash
   git clone https://github.com/jacobiwoop/Tunfox.git
   cd Tunfox
   chmod +x tunfox
   ```

2. **Test immédiat** :
   ```bash
   ./tunfox -p 8000  # Expose le port 8000 local
   ```

3. **Installation permanente** :
   ```bash
   sudo cp tunfox /usr/local/bin/
   tunfox --help  # Utilisable partout
   ``` sans installation

#### Option 1: Exécutable binaire
```bash
# Directement depuis le dossier
chmod +x tunfox
./tunfox --help
```

#### Option 2: Script Python
```bash
# Si l'exécutable ne fonctionne pas
python tunfox.py --help
python3 tunfox.py --help
```

## 🔧 Utilisation

## 🔧 Utilisation

### Utilisation basique

Pour exposer un service local sur le port 3000 (par défaut) :
```bash
# Avec l'exécutable  
tunfox

# Ou avec Python si nécessaire
python tunfox.py
```

*Note: Remplacez `tunfox` par `./tunfox` si vous n'avez pas installé dans le PATH*

### Exemples d'utilisation

#### Avec l'exécutable tunfox  
```bash
tunfox -p 8080
tunfox -t mon-api -p 5000
tunfox --tunnel webapp --port 3000 --verbose
tunfox --host 192.168.1.100 --port 8000
```

#### Avec le script Python 
```bash
python tunfox.py -p 8080
python tunfox.py -t mon-api -p 5000
python tunfox.py --tunnel webapp --port 3000 --verbose
python tunfox.py --host 192.168.1.100 --port 8000
```

## ⚙️ Options disponibles

| Option | Raccourci | Description | Défaut |
|--------|-----------|-------------|---------|
| `--tunnel` | `-t` | Nom du tunnel/sous-domaine | Généré aléatoirement |
| `--port` | `-p` | Port du service local | 3000 |
| `--host` | | Host du service local | localhost |
| `--verbose` | `-v` | Mode verbose (logs détaillés) | Désactivé |

## 📊 Affichage des informations

Au démarrage, le client affiche :
```
tunfox ...
============================================================
📡 Serveur WebSocket: ws://3.15.215.220:8765
🌐 Tunnel public:     https://abc123def.aiko.qzz.io
🏠 Service local:     http://localhost:3000
📊 Mode verbose:      Désactivé
============================================================
💡 Appuyez sur Ctrl+C pour arrêter le tunnel
```

## 🔄 Fonctionnement

1. **Connexion** : Le client se connecte au serveur WebSocket
2. **Enregistrement** : Demande de création du sous-domaine
3. **Activation** : Le tunnel devient actif et accessible publiquement
4. **Proxy** : Les requêtes HTTPS sont transmises vers votre service local
5. **Réponses** : Les réponses de votre service sont renvoyées aux clients

## 🛡️ Gestion des erreurs

Le client gère automatiquement :
- **Connexions refusées** : Reconnexion automatique (5 tentatives max)
- **Services locaux indisponibles** : Retourne une erreur 502
- **Timeouts** : Retourne une erreur 504 après 10 secondes
- **Déconnexions** : Reconnexion transparente

## 📝 Logs et débogage

### Mode normal
```
2024-01-15 10:30:15 - INFO - Connexion au serveur...
2024-01-15 10:30:16 - INFO - Tunnel abc123def.aiko.qzz.io activé avec succès!
```

### Mode verbose (`-v`)
```
2024-01-15 10:30:20 - INFO - Requête GET /api/users
2024-01-15 10:30:21 - INFO - Réponse: 200
```

## 🚪 Arrêt du tunnel

Pour arrêter le tunnel proprement :
- Appuyez sur **Ctrl+C**
- Ou envoyez un signal SIGTERM au processus

## 🌐 Cas d'usage

### Développement web
```bash
# Serveur de développement React (port 3000)
tunfox -t mon-app

# API Node.js (port 8080)
tunfox -t api-dev -p 8080
```

### Tests et démonstrations
```bash
# Partager une démo rapidement
tunfox -t demo-client -p 5000 -v
```

### Services backend
```bash
# Base de données avec interface web
tunfox -t db-admin -p 8081

# Service de monitoring
tunfox -t monitoring -p 9090
```

## ⚠️ Notes importantes

- **Sécurité** : Ne pas exposer de services sensibles sans authentification
- **Performance** : Les requêtes passent par le serveur proxy officiel
- **Disponibilité** : Le service dépend de la disponibilité du serveur tunnel
- **Nom de domaine** : Format automatique `{tunnel}.aiko.qzz.io`
- **Serveur fixe** : Utilise le serveur officiel TunFox (pas de configuration serveur)

## 🐛 Résolution de problèmes

### L'exécutable ne fonctionne pas
```bash
# Solution 1: Utiliser le script Python
python tunfox.py --help

# Solution 2: Vérifier les permissions
chmod +x tunfox
./tunfox --help

# Solution 3: Installer les dépendances
pip install -r requirements.txt
python tunfox.py --help
```

### Service local indisponible
```
Erreur: Service local indisponible sur http://localhost:3000
Solution: Vérifiez que votre service est démarré sur le bon port
```

### Connexion refusée
```
Erreur: Connexion refusée (tentative 1/5)
Solution: Vérifiez votre connexion internet et la disponibilité du serveur TunFox
```

### URL WebSocket invalide
```
Erreur: URL WebSocket invalide
Solution: Problème de configuration interne, redémarrez TunFox ou contactez le support
```

## 📞 Support

En cas de problème :
1. Utilisez le mode verbose (`-v`) pour plus de détails
2. Vérifiez que votre service local fonctionne
3. Testez la connectivité internet
4. Le serveur TunFox est configuré automatiquement

---

**TunFox** - Exposez vos services locaux en toute simplicité ! 🦊

....with ❤️ by aiko 🦊
