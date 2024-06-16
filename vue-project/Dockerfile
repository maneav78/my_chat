FROM node:lts-alpine

WORKDIR /app

COPY . .

RUN npm install
RUN npm install vue-socket.io --save

COPY . .

EXPOSE 8080
CMD [ "npm", "run", "serve" ]