import express from "express";

const app = express();
const PORT = process.env.APP_PORT || 3000;

app.get("/api", (req, res) => {
  res.json({ message: "Day 5 system running" });
});

app.get("/api/health", (req, res) => {
  res.json({ status: "ok" });
});

app.listen(PORT, () => {
  console.log(`Backend running on ${PORT}`);
});
