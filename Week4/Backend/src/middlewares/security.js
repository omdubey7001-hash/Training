import express from "express";
import helmet from "helmet";
import cors from "cors";
import rateLimit from "express-rate-limit";

export function applySecurity(app) {
  // Secure HTTP headers
  app.use(helmet());

  // CORS policy
  app.use(
    cors({
      origin: "*",
      methods: ["GET", "POST", "PUT", "DELETE"]
    })
  );

  // Rate limiting
  app.use(
    rateLimit({
      windowMs: 15 * 60 * 1000,
      max: 30,
      message: "Too many requests, try again later"
    })
  );

  // Payload size limit
  app.use(express.json({ limit: "10kb" }));
}
