import http from "http";
import config from "./config/index.js";
import logger from "./utils/logger.js";
import connectDB from "./loaders/db.js";
import createApp from "./loaders/app.js";

async function startServer() {
  try {
    await connectDB();

    const app = createApp();

    const server = http.createServer(app);

    server.listen(config.port, () => {
      logger.info(`Server started on port ${config.port}`);
    });


    process.on("SIGTERM", shutdown);
    process.on("SIGINT", shutdown);

    function shutdown() {
      logger.info("Shutting down server...");
      server.close(() => {
        logger.info("Server closed");
        process.exit(0);
      });
    }
  } catch (err) {
    logger.error("Startup failed", err);
    process.exit(1);
  }
}

startServer();