# Pull a base image
FROM node:10-alpine

# Create a working directory for the django project
WORKDIR /code/client

# Install the dependencies to the container
COPY package.json yarn.lock /code/client/
RUN yarn install
RUN yarn global add serve

# Copy front end to container
ADD . /code/client/

# Build and deploy
RUN yarn run build

# Open a port on the container
EXPOSE 5000
