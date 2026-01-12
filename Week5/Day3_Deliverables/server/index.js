import express from "express";
import os from "os";

const app = express();
const PORT = process.env.PORT || 3000;

app.get("/api", (req, res) => {
  res.json({
    message: "Hello from backend",
    pid: process.pid,
    server:os.hostname()
  });
});

app.listen(PORT, () => {
  console.log(`Backend running on port ${PORT}, PID ${process.pid}`);
});
