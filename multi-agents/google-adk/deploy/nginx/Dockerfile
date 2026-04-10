FROM nginx:1.26-alpine

RUN apk add --no-cache openssl

COPY nginx.conf /etc/nginx/nginx.conf
COPY docker-entrypoint.d/40-adk-auth.sh /docker-entrypoint.d/40-adk-auth.sh
RUN chmod +x /docker-entrypoint.d/40-adk-auth.sh
