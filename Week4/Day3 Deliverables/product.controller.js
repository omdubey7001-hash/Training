import ProductService from "../services/product.service.js";

class ProductController {
  async create(req, res, next) {
    try {
      const product = await ProductService.createProduct(req.body);
      res.status(201).json({ success: true, data: product });
    } catch (err) {
      next(err);
    }
  }

  async getAll(req, res, next) {
    try {
      const result = await ProductService.getProducts(req.query);
      res.json({ success: true, ...result });
    } catch (err) {
      next(err);
    }
  }

  async getById(req, res, next) {
    try {
      const product = await ProductService.getProductById(req.params.id);
      res.json({ success: true, data: product });
    } catch (err) {
      next(err);
    }
  }

  async delete(req, res, next) {
    try {
      const product = await ProductService.deleteProduct(req.params.id);
      res.json({ success: true, data: product });
    } catch (err) {
      next(err);
    }
  }
}

export default new ProductController();
