FROM node:18-alpine

WORKDIR /app

COPY package.json .

RUN npm install

COPY . .

RUN npm run build

# Install a lightweight static file server.
RUN npm install -g serve

EXPOSE 8080

# Command to serve the build output.
CMD ["serve", "-s", "dist", "-l", "8080"]