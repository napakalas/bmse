FROM node:14.14.0

WORKDIR /vue_app

RUN npm install

COPY ./vue .

RUN pwd

RUN ls -la

RUN npm install axios

#RUN vue add vuetify@2.6.6
RUN npm install vuetify@2.6.6

RUN npm i vue-router@3.5.1

RUN npm i vue-katex katex -P

RUN npm install vue-carousel

#RUN npm run build
CMD ["npm", "run", "serve"]
