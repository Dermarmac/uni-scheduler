FROM node:18-alpine

WORKDIR /app

COPY . /app

RUN npm install && npm run build

EXPOSE 80

CMD [ "npx", "vite", "preview", "--port", "80", "--host" ]
