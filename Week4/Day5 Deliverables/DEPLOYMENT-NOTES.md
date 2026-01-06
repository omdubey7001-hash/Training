# ASYNC JOBS & OBSERVABILITY — Day 5  
**Week 4: Backend Engineering**

---

## 1. Overview

This document explains how asynchronous jobs, queues, workers, and observability
are implemented in the backend system.

The goal of Day-5 is to ensure that **heavy or slow operations do not block API responses**
and that the system can be **observed, monitored, and debugged in production**.

---

## 2. Why Asynchronous Jobs Are Required

In a synchronous system:

Client → API → Heavy Work → Response (slow)

This causes:
- Slow API responses
- Poor user experience
- Request timeouts under load

---

With asynchronous jobs:

Client → API → Job Queued → Response (fast)  
                             ↓  
                       Worker processes job

This ensures:
- APIs remain fast
- Heavy work runs in background
- System scales better

---

## 3. Use Cases for Async Jobs

Asynchronous jobs are used for:
- Email sending
- Notifications
- Background processing
- Logging and analytics
- Order or product post-processing

In this system, async jobs are triggered when a **product is created**.

---

## 4. Job Queue Architecture

The system uses a **queue-based architecture**.

### Components
- Queue: Stores pending jobs
- Worker: Processes jobs one by one
- Service Layer: Pushes jobs into the queue

---

### Flow Diagram

Client  
↓  
Controller  
↓  
Service (adds job to queue)  
↓  
Queue  
↓  
Worker (processes job asynchronously)

---

## 5. Queue Implementation

A queue is responsible for:
- Holding jobs
- Executing them in order
- Preventing concurrent execution conflicts

Each job is added to the queue and processed independently of the API request lifecycle.

This ensures that API responses are **non-blocking**.

---

## 6. Worker Implementation

A worker is responsible for:
- Receiving job data
- Performing heavy or slow tasks
- Logging success or failure

In this system, the worker:
- Simulates a heavy task using delay
- Logs when product processing is completed

Workers do not return responses to clients.

---

## 7. Non-Blocking API Behavior

When a product is created:
- The product is saved in the database
- An async job is added to the queue
- The API responds immediately

The client does **not wait** for the worker to finish.

This confirms:
- Correct async behavior
- Proper separation of concerns

---

## 8. Observability

Observability answers the question:

> “What is my system doing right now?”

It consists of:
- Logs
- Metrics
- Health checks

---

## 9. Logging

Logs are used to track:
- Job creation
- Job execution
- Job completion
- Job failure

Structured logs make debugging easier in production environments.

Logging ensures visibility into background processing.

---

## 10. Metrics

Metrics provide numerical insights into system behavior.

Tracked metrics include:
- Total jobs added
- Completed jobs
- Failed jobs

Metrics are stored in memory and reset on server restart.

They help answer:
- How many jobs ran?
- How many failed?
- Is the system healthy?

---

## 11. Health Endpoint

A health endpoint is exposed to monitor system status.

The endpoint returns:
- Server uptime
- Memory usage
- Job metrics

This endpoint is used by:
- Developers
- Monitoring tools
- Deployment systems

---

## 12. Failure Handling

If a job fails:
- The error is logged
- Failure metrics are updated
- The API remains unaffected

This ensures:
- Fault isolation
- System stability
- Safe error handling

---

## 13. Benefits of This Design

This async job architecture provides:
- Fast API responses
- Background task processing
- Better scalability
- Production-grade observability
- Easier debugging and monitoring

---

## 14. Conclusion

Day-5 completes the backend system by introducing:
- Asynchronous processing
- Job queues and workers
- Observability through logs, metrics, and health checks

The backend is now:
- Non-blocking
- Scalable
- Observable
- Production-ready
