import { Queue } from "bullmq";
import connection from "./redis.connection.js";

export const productQueue = new Queue("product-queue", {
  connection
});
