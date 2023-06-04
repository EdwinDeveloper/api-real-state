#!/bin/sh

set -e

# Function to run Certbot for certificate renewal
#renew_certificates() {
#    certbot renew --nginx
#}

# Generate and substitute the environment variables in the NGINX config
envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf

# Check if the certificates need renewal
#if [ -f "/etc/letsencrypt/live/example.com/fullchain.pem" ] && [ -f "/etc/letsencrypt/live/example.com/privkey.pem" ]; then
    # Certificates exist, check if renewal is needed
#    certbot renew --dry-run || renew_certificates
#else
    # Certificates don't exist, obtain new ones
#    certbot certonly --standalone -d example.com -d www.example.com --non-interactive --agree-tos -m edwindeveloper@outlook.com
#fi

# Start Nginx
nginx -g 'daemon off;'
