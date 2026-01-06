import express from "express";
import { jobMetrics } from "../metrics/job.metrics.js";

const router = express.Router();

router.get("/health", (req, res) => {
  res.json({
    status: "OK",
    uptimeInSeconds: process.uptime(),
    memoryUsage: process.memoryUsage(),
    jobMetrics
  });
});

export default router;
