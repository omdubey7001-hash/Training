import logger from "../utils/logger.js";

export const sendEmailJob = async ({ to, subject }) => {
  try {
    // Simulate email delay
    await new Promise(resolve => setTimeout(resolve, 1500));

    logger.info("Email sent successfully", {
      to,
      subject
    });
  } catch (error) {
    logger.error("Email job failed", {
      error: error.message
    });
    throw error;
  }
};
