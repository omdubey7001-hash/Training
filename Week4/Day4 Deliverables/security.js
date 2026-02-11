import express from "express";
import helmet from "helmet";
import cors from "cors";
import rateLimit from "express-rate-limit";
import mongoSanitize from "express-mongo-sanitize";
import xss from "xss-clean";
import hpp from "hpp";

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
  app.use(express.urlencoded({ extended: true, limit: "10kb" }));

  //NoSQL injection
  app.use(
    mongoSanitize({
      replaceWith: "_"
    })
  );

  //XSS Protection
  app.use(xss());

  //Parameter Pollution Protection
  app.use(
    hpp({
      whitelist: ["tags"] 
    })
  );
}
