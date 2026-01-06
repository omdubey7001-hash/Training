export const validate =
  (schema) =>
  (req, res, next) => {
    try {
      req.body = schema.parse(req.body);
      next();
    } catch (err) {
      return res.status(400).json({
        success: false,
        message: "Validation failed",
        errors: err.errors,
        code: "VALIDATION_ERROR",
        timestamp: new Date().toISOString(),
        path: req.originalUrl
      });
    }
  };
