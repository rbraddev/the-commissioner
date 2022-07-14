FROM node:alpine as builder

WORKDIR /app
COPY ./frontend .

RUN npm install -g @quasar/cli
RUN npm install && npm install --dev-only && quasar build

FROM nginx:alpine as production
COPY --from=builder /app/dist/spa /usr/share/nginx/html
COPY ./frontend/docker/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]