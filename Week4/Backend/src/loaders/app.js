import { applySecurity } from "../middlewares/security.js";
import express from "express";
import logger from "../utils/logger.js";
import productRoutes from "../routes/product.routes.js";
import errorMiddleware from "../middlewares/error.middleware.js";
import healthRoutes from "../routes/health.routes.js";
import requestId from "../middlewares/requestId.js";
import { tracingMiddleware } from "../utils/tracing.js";




export default function createApp() {
  const app = express();

  app.use(express.json());
  app.use(express.urlencoded({ extended: true }));

  logger.info("Middlewares loaded");
  applySecurity(app);
  app.use(requestId);
  app.use(tracingMiddleware);
  app.use("/api", healthRoutes);
  app.use("/api", productRoutes);
  app.use(errorMiddleware);
  let routeCount = 0;

  const router = express.Router();


  router.get("/health", (req, res) => {
    res.json({ status: "OK" });
  });

  routeCount = router.stack.length;

  app.use("/api", router);

  logger.info(`Routes mounted: ${routeCount} endpoints`);

  return app;
}
