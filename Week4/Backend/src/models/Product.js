import mongoose from "mongoose";

const productSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
      trim: true
    },

    description: {
      type: String,
      trim: true
    },

    price: {
      type: Number,
      required: true,
      min: 0
    },

    tags: {
      type: [String],
      default: []
    },

    status: {
      type: String,
      enum: ["ACTIVE", "INACTIVE"],
      default: "ACTIVE"
    },

    deletedAt: {
      type: Date,
      default: null
    }
  },
  { timestamps: true }
);

productSchema.index({ status: 1, createdAt: -1 });

const Product = mongoose.model("Product", productSchema);
export default Product;
