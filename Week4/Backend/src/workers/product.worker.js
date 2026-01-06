import logger from "../utils/logger.js";

export const productCreatedWorker = async (product) => {
  logger.info("Processing product job", { productId: product._id });

  // Simulate heavy work
  await new Promise(resolve => setTimeout(resolve, 2000));

  logger.info("Product job completed", { productName: product.name });
};
