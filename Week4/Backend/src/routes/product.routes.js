import express from "express";
import ProductController from "../controllers/product.controller.js";

const router = express.Router();

router.post("/products", ProductController.create);
router.get("/products", ProductController.getAll);
router.get("/products/:id", ProductController.getById);
router.delete("/products/:id", ProductController.delete);

export default router;
