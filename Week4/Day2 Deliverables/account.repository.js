import Account from "../models/Account.js";
import mongoose from "mongoose";

class AccountRepository {
  async create(data) {
    return Account.create(data);
  }

  async findById(id) {
    if (!mongoose.Types.ObjectId.isValid(id)) return null;
    return Account.findById(id);
  }


  async findPaginated({ limit = 10, cursor }) {
    const query = {};

    if (cursor) {
      query._id = { $lt: cursor };
    }

    const results = await Account.find(query)
      .sort({ _id: -1 })
      .limit(limit + 1);

    const hasMore = results.length > limit;
    if (hasMore) results.pop();

    return {
      data: results,
      nextCursor: hasMore ? results[results.length - 1]._id : null
    };
  }

  async update(id, data) {
    return Account.findByIdAndUpdate(id, data, {
      new: true,
      runValidators: true
    });
  }

  async delete(id) {
    return Account.findByIdAndDelete(id);
  }
}

export default new AccountRepository();
