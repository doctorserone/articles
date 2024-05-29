FROM nginx:alpine

ADD ./server/default.conf /etc/nginx/conf.d
ADD ./app/src/static /var/www/html/static

CMD [ "nginx", "-g", "daemon off;" ]
