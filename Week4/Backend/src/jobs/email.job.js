import logger from "../utils/logger.js";
import {productQueue} from "../queues/product.queue.js"
export const sendEmailJob = async ({ to, subject,body,requestId}) => {
  try {
    await productQueue.add("send-email", {
      to,
      subject,
      body,
      requestId
    });
  } catch (error) {
    logger.error("Email job failed", {
      error: error.message
    });
    throw error;
  }
};
