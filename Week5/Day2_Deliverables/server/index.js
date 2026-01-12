import express from "express";
import mongoose from "mongoose";

const app = express();
const PORT = process.env.PORT || 5000;
const MONGO_URI = process.env.MONGO_URI;


async function connectDB() {
  try {
    await mongoose.connect(MONGO_URI);
    console.log("MongoDB connected");
  } catch (err) {
    console.error("MongoDB connection failed:", err.message);
    process.exit(1);
  }
}

connectDB();

app.use(express.json());

app.get("/", (req, res) => {
  res.json({
    status: "OK",
    message: "Server is running",
  });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
