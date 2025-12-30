import Order from "../models/Order.js";
import mongoose from "mongoose";

class OrderRepository {
  async create(data) {
    return Order.create(data);
  }

  async findById(id) {
    if (!mongoose.Types.ObjectId.isValid(id)) return null;
    return Order.findById(id).populate("accountId");
  }


  async findPaginated({ limit = 10, cursor }) {
    const query = {};

    if (cursor) {
      query._id = { $lt: cursor };
    }

    const results = await Order.find(query)
      .sort({ _id: -1 })
      .limit(limit + 1)
      .populate("accountId");

    const hasMore = results.length > limit;
    if (hasMore) results.pop();

    return {
      data: results,
      nextCursor: hasMore ? results[results.length - 1]._id : null
    };
  }

  async update(id, data) {
    return Order.findByIdAndUpdate(id, data, {
      new: true,
      runValidators: true
    });
  }

  async delete(id) {
    return Order.findByIdAndDelete(id);
  }
}

export default new OrderRepository();
