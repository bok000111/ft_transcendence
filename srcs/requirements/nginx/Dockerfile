FROM alpine:3.19

RUN apk update && apk upgrade --no-cache
RUN apk add --no-cache nginx openssl dumb-init

COPY ./conf/ft_transcendence.conf /etc/nginx/http.d

RUN mkdir -p /etc/ssl/certs /etc/ssl/private

RUN openssl req -x509 -days 365 -nodes -newkey rsa:2048 \
        -keyout /etc/ssl/private/nginx.key \
        -out /etc/ssl/certs/nginx.crt \
		-subj "/C=KR/ST=Seoul/L=Seoul/O=42Seoul/CN=${DOMAIN}"

EXPOSE 443

ENTRYPOINT [ "dumb-init", "--" ]
CMD ["nginx", "-g", "daemon off;"]
# CMD ["tail", "-f", "/dev/null"]