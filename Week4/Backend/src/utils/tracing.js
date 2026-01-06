import { randomUUID } from "crypto";

export const tracingMiddleware = (req, res, next) => {
  const traceId = randomUUID();

  req.traceId = traceId;
  res.setHeader("X-Trace-Id", traceId);

  next();
};
