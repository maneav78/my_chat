FROM node:lts-alpine

WORKDIR /app

COPY . .

RUN npm install 
RUN npm install vue-socket.io --save
RUN npm install cors --save
RUN npm install socket.io-client@latest


EXPOSE 8080
CMD [ "npm", "run", "serve" ]