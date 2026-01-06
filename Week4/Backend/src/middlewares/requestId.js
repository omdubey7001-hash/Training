import { randomUUID } from "crypto";

export default function requestId(req, res, next) {
  req.requestId = randomUUID();
  res.setHeader("X-Request-ID", req.requestId);
  next();
}
