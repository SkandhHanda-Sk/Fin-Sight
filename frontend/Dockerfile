# Testing/frontend/Dockerfile (Corrected Version)
# Use the current Long-Term Support (LTS) version of Node.js
FROM node:lts-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install app dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Make port 5173 available (the default Vite port)
EXPOSE 5173

# Command to run the Vite development server
CMD ["npm", "run", "dev"]