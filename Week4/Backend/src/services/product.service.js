import ProductRepository from "../repositories/product.repository.js";
import jobQueue from "../queues/job.queue.js";
import { productCreatedWorker } from "../workers/product.worker.js";

class ProductService {

  async createProduct(data) {

    const product = await ProductRepository.create(data);


    jobQueue.add(
      () => productCreatedWorker(product),
      {
        attempts: 3,
        backoff: 2000
      }
    );


    return product;
  }

  async getProductById(id) {
    const product = await ProductRepository.findById(id);
    if (!product) {
      const error = new Error("Product not found");
      error.code = "PRODUCT_NOT_FOUND";
      error.status = 404;
      throw error;
    }
    return product;
  }

  async getProducts(query) {
    return ProductRepository.findWithFilters(query);
  }

  async deleteProduct(id) {
    const product = await ProductRepository.softDelete(id);
    if (!product) {
      const error = new Error("Product not found");
      error.code = "PRODUCT_NOT_FOUND";
      error.status = 404;
      throw error;
    }
    return product;
  }
}

export default new ProductService();
