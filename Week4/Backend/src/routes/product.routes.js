import express from "express";
import ProductController from "../controllers/product.controller.js";
import { validate } from "../middlewares/validate.js";
import { createProductSchema } from "../validators/product.validator.js";

const router = express.Router();

router.post(
  "/products",
  validate(createProductSchema),
  ProductController.create
);

router.get("/products", ProductController.getAll);
router.get("/products/:id", ProductController.getById);
router.delete("/products/:id", ProductController.delete);

export default router;
