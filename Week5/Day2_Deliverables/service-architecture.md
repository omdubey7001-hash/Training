# Service Architecture — Docker Compose

## Overview
This application is a multi-container setup using Docker Compose.
It consists of three services:

- React Client
- Node.js Server
- MongoDB Database

All services run in isolated containers and communicate via Docker networking.

---

## Services

### 1. Client (React)
- Runs on port `3000`
- Built from `./client`
- Communicates with the Node server via HTTP

### 2. Server (Node.js)
- Runs on port `5000`
- Built from `./server`
- Connects to MongoDB using internal Docker DNS
- Mongo connection string:

`mongodb://mongo:27017/appdb`


### 3. MongoDB
- Official MongoDB image
- Data stored using Docker volume
- Persistent across container restarts

---

## Networking
- All services are connected to a custom bridge network
- Containers resolve each other using service names

---

## Volumes
- `mongo-data` stores MongoDB data persistently
- Server logs mapped to host directory

---

## Logs
- Logs are accessible using:
`docker compose logs server`


---

## Startup
All services are started using a single command:

`docker compose up -d`