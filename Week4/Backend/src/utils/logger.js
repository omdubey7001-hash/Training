import winston from "winston";
import path from "path";
import config from "../config/index.js";

const logFilePath = path.join(process.cwd(), "logs", "app.log");

const logger = winston.createLogger({
  level: config.logLevel,
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({
      filename: logFilePath,
    }),
  ],
});

export default logger;
