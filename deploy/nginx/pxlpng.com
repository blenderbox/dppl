server {
  server_name pxlpng.com
  listen *:80;

  # Logs
  access_log /var/www/pxlpng.com/log/nginx/access.log;
  error_log /var/www/pxlpng.com/log/nginx/error.log;

  charset utf-8;

  root /var/www/pxlpng.com/public/;

  # Static files
  location ~* ^/(media|static)/.*\.(?:jpg|jpeg|gif|png|ico)$ {
    expires 1M;
    access_log off;
    add_header Cache-Control "public";
  }
  location ~* ^/(media|static)/.*\.(?:css|js)$ {
    expires 1y;
    access_log off;
    add_header Cache-Control "public";
  }
  location ~* ^/(media|static)/.*\.(?:ttf|ttc|otf|eot|woff)$ {
    expires 1M;
    access_log off;
    add_header Cache-Control "public";
  }
  location ~ ^/(media|static)/ {
    expires 1d;
    access_log off;
    add_header Cache-Control "public";
  }

  location ~ ^/(robots\.txt|humans\.txt|favicon\.ico|apple-touch-icon\.png)$ {
    alias /var/www/pxlpng.com/public/static/$1;
    expires 1w;
    access_log on;
    add_header Cache-Control "public";
  }

  location / {
    proxy_pass http://127.0.0.1:9000;
    include /etc/nginx/proxy_params;
    add_header "X-UA-Compatible" "IE=Edge,chrome=1";
  }
}
