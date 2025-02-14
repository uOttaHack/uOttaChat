#!/bin/bash

# -----------------------------
# 1) CONFIGURATION
# -----------------------------
DOMAIN1="chat.uottahack.ca"
DOMAIN2="chat-staging.uottahack.ca"
PORT="3001"    # Port your FastAPI app will listen on
FASTAPI_APP="app.py"     # Path to your FastAPI file
DISCORD_BOT="bot.py"     # Path to your Discord bot file

# -----------------------------
# 2) SYSTEM & NGINX SETUP
# -----------------------------
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

echo "Installing NGINX, Certbot, and Python3..."
sudo apt install -y nginx certbot python3-certbot-nginx python3-pip

# -----------------------------
# 3) CONFIGURE NGINX FOR DOMAINS
# -----------------------------
echo "Configuring NGINX for $DOMAIN1 and $DOMAIN2..."

# Create NGINX config for DOMAIN1
cat <<EOF | sudo tee /etc/nginx/sites-available/$DOMAIN1
server {
    listen 80;
    server_name $DOMAIN1;

    location / {
        proxy_pass http://127.0.0.1:$PORT;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

# Enable the site for DOMAIN1
sudo ln -sf /etc/nginx/sites-available/$DOMAIN1 /etc/nginx/sites-enabled/$DOMAIN1

# Create NGINX config for DOMAIN2
cat <<EOF | sudo tee /etc/nginx/sites-available/$DOMAIN2
server {
    listen 80;
    server_name $DOMAIN2;

    location / {
        proxy_pass http://127.0.0.1:$PORT;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

# Enable the site for DOMAIN2
sudo ln -sf /etc/nginx/sites-available/$DOMAIN2 /etc/nginx/sites-enabled/$DOMAIN2

# Test and reload NGINX
sudo nginx -t
sudo systemctl reload nginx

# -----------------------------
# 4) OBTAIN SSL CERTIFICATES
# -----------------------------
echo "Obtaining SSL certificates via Certbot..."
sudo certbot --nginx -d $DOMAIN1 -d $DOMAIN2 --non-interactive --agree-tos -m youremail@example.com

# Enable auto-renewal
sudo systemctl enable --now certbot.timer

# Restart NGINX
sudo systemctl restart nginx

echo "NGINX has been configured for $DOMAIN1 and $DOMAIN2 with SSL."

# -----------------------------
# 5) PYTHON DEPENDENCIES
# -----------------------------
echo "Installing Python dependencies..."
pip3 install --user -r requirements.txt

# -----------------------------
# 6) LAUNCH FASTAPI & DISCORD BOT
# -----------------------------
echo "Launching FastAPI on port $PORT..."

# Run FastAPI in the background
nohup python3 "$FASTAPI_APP" > fastapi.log 2>&1 &

echo "Launching Discord Bot..."

# Run Discord Bot in the background
nohup python3 "$DISCORD_BOT" > discordbot.log 2>&1 &

echo "All services have been started successfully!"