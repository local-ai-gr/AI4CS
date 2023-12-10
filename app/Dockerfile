FROM node:18-alpine

WORKDIR /usr/src/app
ENV PATH /usr/src/app/node_modules/.bin:$PATH

COPY package*.json ./

RUN npm install

COPY . .
RUN chmod 777 node_modules

EXPOSE 3000

CMD ["npm", "run", "dev"]