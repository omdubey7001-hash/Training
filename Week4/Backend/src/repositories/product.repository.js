import Product from "../models/Product.js";

class ProductRepository {
  async create(data) {
    return Product.create(data);
  }

  async findById(id, { includeDeleted = false } = {}) {
    const query = { _id: id };
    if (!includeDeleted) query.deletedAt = null;

    return Product.findOne(query);
  }

  async findWithFilters({
    search,
    minPrice,
    maxPrice,
    tags,
    sort = "createdAt:desc",
    limit = 10,
    cursor,
    includeDeleted = false
  }) {
    const query = {};

    if (!includeDeleted) {
      query.deletedAt = null;
    }

    if (search) {
      query.$or = [
        { name: { $regex: search, $options: "i" } },
        { description: { $regex: search, $options: "i" } }
      ];
    }

    if (minPrice || maxPrice) {
      query.price = {};
      if (minPrice) query.price.$gte = Number(minPrice);
      if (maxPrice) query.price.$lte = Number(maxPrice);
    }

    if (tags) {
      query.tags = { $in: tags.split(",") };
    }

    if (cursor) {
      query._id = { $lt: cursor };
    }

    const [field, direction] = sort.split(":");
    const sortQuery = { [field]: direction === "asc" ? 1 : -1 };

    const results = await Product.find(query)
      .sort(sortQuery)
      .limit(Number(limit) + 1);

    const hasMore = results.length > limit;
    if (hasMore) results.pop();

    return {
      data: results,
      nextCursor: hasMore ? results[results.length - 1]._id : null
    };
  }

  async softDelete(id) {
    return Product.findByIdAndUpdate(
      id,
      { deletedAt: new Date() },
      { new: true }
    );
  }
}

export default new ProductRepository();
