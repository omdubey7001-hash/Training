# SECURITY REPORT — Day 4  
**Week 4: Backend Engineering**

---

## 1. Overview

This document summarizes the security measures implemented in the backend APIs
and the results of manual security testing performed on Day-4.

The objective of Day-4 is to ensure that the application is protected against
common attacks and misuse before requests reach business logic or the database.

---

## 2. Security Controls Implemented

The following security layers were added to the application:

- Input validation using **Zod**
- Payload whitelisting and sanitization
- HTTP security headers using **Helmet**
- Cross-Origin Resource Sharing (CORS) policy
- Rate limiting to prevent abuse
- NoSQL injection protection
- Cross-Site Scripting (XSS) protection
- Request payload size limiting

---

## 3. Validation Testing (Zod)

### Test Case: Invalid Input

**Input**
```json
{
  "name": "",
  "price": -100
}
```

- Expected Result

    - Request should be rejected

    - Validation error should be returned

- Actual Result

    - Request blocked with HTTP 400

    - Validation error message returned

- Status
✔ Passed

--- 

## 4. NoSQL Injection Testing

### Test Case: MongoDB Injection Payload

Input

```
{
  "name": { "$gt": "" },
  "price": 100
}
```

- Expected Result

    - Script content should be sanitized or rejected

- Actual Result

    - Script removed or request rejected

    - No script execution occurred

- Status
✔ Passed

## 5. XSS Attack Testing
### Test Case: Script Injection

**Input**
```
{
  "name": "<script>alert('xss')</script>",
  "price": 100
}
```

- Expected Result

    - Script content should be sanitized or rejected

- Actual Result

    - Script removed or request rejected

    - No script execution occurred

- Status
✔ Passed

--- 

## 6. Payload Size Limit Testing

### Test Case: Oversized Request Body

- Input

    - JSON payload larger than 10KB

- Expected Result

    - Request should be blocked

- Actual Result

    - Server responded with payload size error

- Status
✔ Passed

--- 

## 7. Rate Limiting Testing

### Test Case: Excessive Requests

- Input

    - More than 100 requests sent within 15 minutes

- Expected Result

    - Requests beyond limit should be blocked

- Actual Result

    - Server responded with HTTP 429 Too Many Requests

- Status
✔ Passed

--- 

## 8. CORS Policy Testing

### Test Case: Cross-Origin Request

- Input

    - API request from a different origin

- Expected Result

    - Request allowed based on configured policy

- Actual Result

    - CORS headers applied correctly

    - Request processed successfully

- Status
✔ Passed

---

## 9. Security Headers Verification

- Implemented Headers

    - X-Content-Type-Options

    - X-Frame-Options

    - X-XSS-Protection

    - Strict-Transport-Security

    - Content-Security-Policy

- Status
✔ Headers correctly applied

---

## 10. Conclusion

All planned security controls for Day-4 were successfully implemented and tested.

The application is now protected against:

- Invalid input

- Injection attacks

- Cross-site scripting

- Excessive request abuse

- Oversized payload attacks