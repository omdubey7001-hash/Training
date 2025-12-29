import mongoose from "mongoose";
import logger from "../utils/logger.js";
import config from "../config/index.js";

export default async function connectDB() {
  try {
    await mongoose.connect(config.databaseUrl);
    logger.info("Database connected");
  } catch (error) {
    logger.error("Database connection failed", error);
    process.exit(1); 
  }
}
