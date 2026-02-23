import express from "express";
import ProductController from "../controllers/product.controller.js";
import { validate } from "../middlewares/validate.js";
import { createProductSchema } from "../validators/product.validator.js";
import { sendEmailJob } from "../jobs/email.job.js";
const router = express.Router();

router.post(
  "/products",
  validate(createProductSchema),
  ProductController.create
);

router.get("/products", ProductController.getAll);
router.get("/products/:id", ProductController.getById);
router.delete("/products/:id", ProductController.delete);
router.delete("/products/soft/:id", ProductController.softDelete);

router.post("/notify", async (req, res, next) => {
  try {
    const { to, subject, body } = req.body;
    const requestId = req.requestId || "no-id";

    await sendEmailJob({ to, subject, body, requestId });

    res.status(200).json({
      message: "Email job queued",
      requestId
    });
  } catch (err) {
    next(err);
  }
});
export default router;
