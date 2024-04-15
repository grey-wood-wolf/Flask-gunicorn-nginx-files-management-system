#!/bin/bash

# deploy_flask_app.sh

# Replace the following variables with your own settings
APP_NAME=app
THREADS=2
NGINX_SITES_AVAILABLE=/etc/nginx/sites-available
NGINX_SITES_ENABLED=/etc/nginx/sites-enabled
PORT=80
DOMAIN=$(hostname -I | cut -d' ' -f1)
GUNICORN_WORKERS=2
GUNICORN_PORT_LIST=($(seq 8000 1 $((8000 + $GUNICORN_WORKERS - 1))))
GUNICORN_SERVERS=$(printf "server localhost:%s;\n    " "${GUNICORN_PORT_LIST[@]}")
GUNICORN_PID=()


# Create Nginx site configuration
echo "Creating Nginx configuration for ${APP_NAME}..."
cat > $NGINX_SITES_AVAILABLE/$APP_NAME << EOF
upstream backend {
    ip_hash;
    $GUNICORN_SERVERS
}

server {
    listen $PORT;
    server_name $DOMAIN;
    client_max_body_size 1000M;

    location / {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade; # 这个头是用来升级连接为 WebSocket
        proxy_set_header Connection "upgrade"; # 这是一个特殊的值，告诉 Nginx 升级连接
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        # WebSocket 专用的超时设置，根据需要调整
        proxy_read_timeout 86400; # 1 day timeout, adjust to suit your needs
    }
}
EOF

# Create symbolic link for Nginx site configuration if it doesn't exist
if [ ! -e $NGINX_SITES_ENABLED/$APP_NAME ]; then
    echo "Creating symbolic link for Nginx configuration..."
    sudo ln -s $NGINX_SITES_AVAILABLE/$APP_NAME $NGINX_SITES_ENABLED/$APP_NAME
else
    echo "Symbolic link for Nginx configuration already exists."
fi

# Restart Nginx to apply the changes
echo "Restarting Nginx..."
sudo nginx -t && sudo systemctl restart nginx

# Start Gunicorn servers
echo "Starting Gunicorn server for ${APP_NAME}..."
# 遍历端口号列表，为每个端口号启动一个 Gunicorn 服务, 并记录pid
for port in "${GUNICORN_PORT_LIST[@]}"; do
    sudo gunicorn -k eventlet -w 1 -b 0.0.0.0:$port $APP_NAME:app --threads $THREADS --timeout 120 &
    GUNICORN_PID+=($!)
done


while true; do
# 查看是否键入了 ctrl+c，如果是则杀死所有的gunicorn进程，否则睡1s
    read -t 1 -n 1 key
    if [[ $key == $'\x03' ]]; then
        echo "Ctrl+C pressed. Killing Gunicorn processes..."
        for pid in "${GUNICORN_PID[@]}"; do
            sudo kill -9 $pid
        done
        break
    else
        sleep 1
    fi
done
