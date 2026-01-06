# Deployment Notes — Week 4 Backend

This document explains how to run, verify, and manage the Week 4 Backend
application.  
The instructions reflect the actual setup used during development and testing.

---

## 1. Prerequisites

Before running the application, ensure the following are installed:

- Node.js (v18 or higher)
- MongoDB (running locally or accessible via URI)
- npm (Node Package Manager)
- PM2 (used for process management)

---

## 2. Environment Configuration

The application is configured using environment variables.

Environment variables can be provided in two ways:
- Through environment files (e.g. `.env.local`)
- Directly via PM2 ecosystem configuration

Required variables:
- `NODE_ENV`
- `PORT`
- `DATABASE_URL`

Example MongoDB URL:
- `mongodb://localhost:27017/week4_backend`

Environment files are local-only and must not be committed to Git.

---

## 3. Installing Dependencies

From the Backend project root, install dependencies:

```bash
npm install
```

This installs all runtime and development dependencies required
to start the server and background workers.

## 4. Running the Application (Local)

To start the application without PM2:
```
NODE_ENV=local node src/index.js
```

- On successful startup, logs will confirm:

      - Database connection

      - Middleware initialization

      - Routes mounted

      - Server started on the configured port

## 5. Running the Application with PM2

The application can also be run using PM2 for process management.

- A production-ready configuration is provided in:

`     prod/ecosystem.config.cjs 
`

- To start the application:
```
      cd prod
      pm2 start ecosystem.config.cjs
```

To apply environment changes:
```
      pm2 restart week4-backend --update-env
```

- To check status:

      `pm2 status`

## 6. Health Check

The application exposes a health endpoint:

`GET /api/health`


- This endpoint returns:

      Application status

      Uptime

      Memory usage

      Background job metrics

It is used to verify that the system is running correctly.

## 7. Background Jobs

Background jobs are executed asynchronously.


Key points:

      Jobs do not block API responses

      Retry and backoff logic is implemented

      Job execution is logged for observability

This ensures better performance and fault tolerance.

## 8. Logging and Observability

Logging is implemented using Winston.

Logs are written to:

`logs/app.log`


Logs include:

      Server lifecycle events

      API activity

      Background job execution

      Error details

PM2 also maintains separate stdout and error logs.

Old logs may remain after restarts and can be cleared using:

`pm2 flush`

## 9. Shutdown

To stop the application:

- Without PM2: press Ctrl + C

- With PM2:

`pm2 stop week4-backend`


This performs a graceful shutdown of the server.

## 10. Notes

      Metrics are stored in memory and reset on restart

      Environment validation ensures required configuration is present

      Logs and health endpoints provide observability
