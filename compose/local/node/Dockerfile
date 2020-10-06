FROM node:12.17-stretch

# TODO: The following turoial shows how to use a multistage build of node to reduce this image from c.700 to c.70mb:
#  https://hasura.io/blog/an-exhaustive-guide-to-writing-dockerfiles-for-node-js-web-apps-bbee6bd2f3c4/
#  Putting this dockerfile as builder at the start of the django dockerfile would be awesome

WORKDIR /app

COPY package*.json /app/
COPY jsconfig.json /app/

# TODO If building for production we'll want to properly install node_modules
#  But presently it's mapped to the host directory, so call install prior to app start
#RUN rm -rf /app/node_modules/* && yarn install
# && npm cache clean--force  May introduce weirdness with react-router

# The locally mounted volume will overwrite these so don't copy (for development, production will need them)
#COPY public ./public
#COPY src ./src

ENV PATH ./node_modules/.bin/:$PATH
