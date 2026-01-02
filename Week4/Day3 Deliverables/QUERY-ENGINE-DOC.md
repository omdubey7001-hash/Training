# QUERY ENGINE DOCUMENTATION — Day 3  
**Week 4: Backend Engineering**

---

## 1. Overview

This document explains how the Product API query engine is designed and how it handles
filtering, searching, pagination, soft deletion, and error handling.

The goal is to build APIs that are **scalable**, **predictable**, and **safe under failure**.

---

## 2. Controller → Service → Repository Flow

The application follows a strict layered architecture:

# QUERY ENGINE DOCUMENTATION — Day 3  
**Week 4: Backend Engineering**

---

## 1. Overview

This document explains how the Product API query engine is designed and how it handles
filtering, searching, pagination, soft deletion, and error handling.

The goal is to build APIs that are **scalable**, **predictable**, and **safe under failure**.

---

## 2. Controller → Service → Repository Flow

The application follows a strict layered architecture:

Client → Controller → Service → Repository → Database


### Controller
- Handles HTTP requests and responses
- Reads query params and request body
- Never talks directly to the database

### Service
- Contains business logic
- Validates rules
- Throws errors (does not send responses)

### Repository
- Interacts with MongoDB
- Builds queries and filters
- No HTTP or Express logic

This separation improves maintainability and testability.

---

## 3. Filtering Logic

The Product API supports **dynamic filtering** using query parameters.

### Supported Filters
- `search`
- `minPrice`
- `maxPrice`
- `tags`
- `sort`

### Search
Search is implemented using case-insensitive regex on:
- `name`
- `description`

If `search` is not provided, it is ignored.

---

### Price Filtering
- `minPrice` → filters products with price ≥ minPrice
- `maxPrice` → filters products with price ≤ maxPrice

Both filters are optional and applied only if present.

---

### Tags Filtering
- Supports multiple tags
- Products matching **any** provided tag are returned
- Implemented using `$in`

---

### Sorting
Sorting is dynamic and passed as:

sort=field:direction


Examples:
- `sort=price:asc`
- `sort=createdAt:desc`

Default sorting:


createdAt:desc


---

## 4. Pagination Strategy (Cursor-Based Pagination)

### Why Cursor Pagination?
Skip/limit pagination becomes slow as data grows.
Cursor-based pagination provides **constant performance**.

---

### How It Works
- Results are fetched using `_id` comparison
- Each response returns a `nextCursor`
- The next request uses this cursor to continue

---

### Example Flow
1. First request:

GET /api/products?limit=5


2. Response includes:
```
{
  "data": [...],
  "nextCursor": "abc123"
}
```
3. Next request:

GET /api/products?limit=5&cursor=abc123

### Benefits

- No skipped records

- No duplicates

- Scales well for large datasets

## 5. Soft Delete Implementation

Products are never permanently deleted.

### How Soft Delete Works

A field deletedAt is added to the schema

- null → product is active

- Date → product is deleted

### API Behavior

- Normal GET requests exclude deleted products

- ?includeDeleted=true includes deleted products

This allows:

- Data recovery

- Audit history

- Safe deletion

## 6. Centralized Error Handling

The application uses a single global error middleware.

### Key Principles

- Controllers do not format errors

- Services throw errors

- Middleware handles response formatting

### Error Response Format

All errors follow this structure:
```
{
  "success": false,
  "message": "Product not found",
  "code": "PRODUCT_NOT_FOUND",
  "timestamp": "2025-01-01T10:00:00Z",
  "path": "/api/products/123"
}
```
### Benefits

- Consistent API responses

- Easier debugging

- Production-safe behavior

## 7. Conclusion

This query engine design ensures:

- Flexible APIs

- High performance at scale

- Clean architecture

- Predictable error handling

The system is ready for real-world usage and future extensions such as
authentication, authorization, and rate limiting.