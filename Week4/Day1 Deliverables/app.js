import express from "express";
import logger from "../utils/logger.js";

export default function createApp() {
  const app = express();

  app.use(express.json());
  app.use(express.urlencoded({ extended: true }));

  logger.info("Middlewares loaded");


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
