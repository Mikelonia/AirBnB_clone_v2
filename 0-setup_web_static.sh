#!/usr/bin/env bash
# Sets up a web server for deployment of web_static. By Okpako Michael

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Create necessary directories if they don't exist
sudo mkdir -p /data/web_static/{releases/test,shared}

# Create the fake HTML file with the desired content
sudo tee /data/web_static/releases/test/index.html <<EOF
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
EOF

# Create the symbolic link
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to handle /hbnb_static URL
sudo tee /etc/nginx/sites-available/default <<EOF
server {
    listen 80 default_server;
    server_name _;
    location /hbnb_static/ {
        alias /data/web_static/current/;
        index index.html;
    }
    location / {
        # Add other configurations here if needed
    }
}
EOF

# Restart Nginx to apply changes
sudo service nginx restart

exit 0

