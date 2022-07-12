FROM node:alpine as builder

WORKDIR /app
COPY ./frontend/package.json ./

RUN npm install @quasar/cli 

COPY ./frontend .

RUN npx quasar build


FROM nginx:alpine as production
COPY --from=builder /app/dist/spa /app

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]