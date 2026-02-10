# Service Architecture — Docker Compose (Day 2)

## Overview
This project uses Docker Compose to run a multi-container application that
represents a real-world production setup.

The architecture consists of three main services:
- Client (React)
- Server (Node.js + Express)
- Database (MongoDB)

All services run in isolated Docker containers and communicate over a single
Docker network created automatically by Docker Compose.

---

## Services Description

### 1. Client (React)
- Runs the frontend application.
- Built using Create React App.
- Exposed to host machine on port 3001.
- Sends HTTP requests to the backend service.

Container:
- Image built from `client/Dockerfile`
- Port mapping: `3001:3000`

---

### 2. Server (Node.js + Express)
- Handles API requests from the client.
- Connects to MongoDB for data storage.
- Exposed to host machine on port 3000.

Database Connection:
- Uses Docker internal DNS.
- Connects using service name, not localhost.

Example:
```js
mongodb://mongo:27017/testdb
```

Container:

- Image built from `server/Dockerfile`

- Port mapping: `3000:3000`

### 3. Database (MongoDB)

- Stores application data.

- Runs using the official MongoDB Docker image.

- Uses Docker volume for persistent storage.

#### Volume:

- `mongo_data:/data/db`

This ensures that data is not lost when containers are restarted or removed.

## Networking

- Docker Compose creates a default bridge network.

- All services are attached to this network automatically.

- Containers communicate using service names as hostnames.

#### Example:

- Server → MongoDB: `mongo`

- Client → Server: `server`

No container uses hardcoded IP addresses.

## Volumes

- A named Docker volume is used for MongoDB data persistence.

- Volume is managed by Docker and survives container restarts.

- Declared in `docker-compose.yml`:
```yaml
volumes:
  mongo_data:
```
## Startup Order

- depends_on is used to control service startup sequence.

- Server starts after MongoDB.

- Client starts after Server.

- Only a single command is required to run the whole project `docker compose up -d`.

## Architecture Flow
```
Browser
↓
Client (React)
↓
Server (Node.js / Express)
↓
MongoDB
```

## Benefits of This Architecture

- Clean separation of concerns.

- Easy local development and testing.

- Mirrors real production environments.

- Scalable and maintainable setup.

- Single-command deployment using Docker Compose.

## Conclusion

This Docker Compose-based architecture demonstrates how modern applications
are deployed using multiple services that communicate securely and efficiently
within containerized environments.