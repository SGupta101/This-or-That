FROM node:18-alpine as builder

WORKDIR /app

# Copy package files and TypeScript configs
COPY package.json vite.config.ts tsconfig.json tsconfig.app.json tsconfig.node.json ./

# Install dependencies
RUN npm install

# Copy source code and public files
COPY src src/
COPY index.html ./
COPY public public/

# Development stage - this is used when target=builder
CMD ["npm", "run", "dev"]

# Production stage
FROM nginx:alpine as production

# Copy the built files to nginx's html directory
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 5173

CMD ["nginx", "-g", "daemon off;"]
