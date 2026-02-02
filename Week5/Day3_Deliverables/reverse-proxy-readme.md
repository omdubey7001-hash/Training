# Reverse Proxy Architecture — Day 3

## Overview
This setup demonstrates a reverse proxy and load balancing architecture
using NGINX inside Docker.

NGINX acts as the single public entry point and forwards requests
to multiple backend instances using round-robin load balancing.

---

## Architecture Flow

Client
  ↓
NGINX (Reverse Proxy)
  ↓
Backend Service (multiple replicas)

---

## Components

### NGINX
- Runs inside a Docker container
- Exposes port 80
- Routes `/api` requests to backend services
- Performs round-robin load balancing

### Backend Service
- Node.js application
- Multiple running instances
- Not exposed directly to the host
- Accessible only through NGINX

---

## Routing Rules

| Request Path | Destination |
|-------------|-------------|
| /api/* | backend-service:3000 |

---

## Load Balancing
- NGINX uses round-robin load balancing by default
- Requests are distributed evenly across backend replicas
- Docker DNS resolves the backend service name to multiple container IPs

---

## Networking
- All containers run on the same Docker bridge network
- Services communicate using service names
- No hardcoded IP addresses are used

---

## Key Principles Demonstrated
- Reverse proxy pattern
- Internal service routing
- Horizontal scaling
- Load balancing simulation
- Single entry point architecture

---

## Summary
This architecture mirrors real production systems where:
- NGINX handles traffic management
- Backends scale horizontally
- Internal services remain private
- Load balancing improves availability
