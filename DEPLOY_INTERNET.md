# 🌐 Gadilix — Mise en ligne sur Internet

## Option 1 — ngrok (GRATUIT, 5 minutes)
Idéal pour démo, tests, partager avec quelqu'un rapidement.

```bash
# 1. Télécharger ngrok → https://ngrok.com/download
# 2. Créer compte gratuit sur ngrok.com
# 3. Dans un terminal, lancer le serveur Gadilix
python main.py

# 4. Dans un 2ème terminal, exposer sur Internet
ngrok http 5000
```
ngrok te donnera une URL publique comme :
`https://abc123.ngrok.io` → accessible depuis n'importe où dans le monde.

---

## Option 2 — VPS (RECOMMANDÉ pour usage réel)
Fonctionne sur DigitalOcean, Hetzner, Contabo, OVH, AWS EC2...
Coût : ~5€/mois.

### Sur ton VPS Ubuntu :

```bash
# 1. Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# 2. Installer Python
sudo apt install -y python3 python3-pip git

# 3. Cloner / uploader ton projet
git clone https://github.com/TON-REPO/gadilix.git
cd gadilix

# 4. Installer les dépendances
pip3 install --only-binary=:all: -r requirements.txt

# 5. Créer fichier .env
cp .env.example .env
nano .env   # Modifier SECRET_KEY, JWT_SECRET_KEY

# 6. Lancer avec Gunicorn (serveur de production)
pip3 install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "server.app:create_app()"
```

### Lancer automatiquement au démarrage (systemd) :

```bash
sudo nano /etc/systemd/system/gadilix.service
```

Contenu :
```ini
[Unit]
Description=Gadilix SOC Platform
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/gadilix
ExecStart=/usr/local/bin/gunicorn -w 4 -b 0.0.0.0:5000 "server.app:create_app()"
Restart=always
Environment="SECRET_KEY=change-me"
Environment="JWT_SECRET_KEY=change-me-jwt"

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable gadilix
sudo systemctl start gadilix
sudo systemctl status gadilix
```

### Nginx (domaine + HTTPS) :

```bash
sudo apt install -y nginx certbot python3-certbot-nginx

# Config Nginx
sudo nano /etc/nginx/sites-available/gadilix
```

```nginx
server {
    server_name gadilix.tondomaine.com;
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/gadilix /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# HTTPS gratuit avec Let's Encrypt
sudo certbot --nginx -d gadilix.tondomaine.com
```

Ton dashboard sera accessible sur `https://gadilix.tondomaine.com` 🔒

---

## Option 3 — Rendre accessible sur ton réseau local

```bash
# Lancer en écoutant sur toutes les interfaces
python main.py
# → accessible sur http://TON_IP_LOCAL:5000
# Trouve ton IP : ipconfig (Windows) ou ip a (Linux)
```

Pour les agents sur d'autres machines du réseau :
```bash
python agent/linux_agent.py --server http://192.168.1.X:5000 --agent-id serveur-web
```

---

## Firewall (VPS)

```bash
# Ouvrir les ports nécessaires
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```
