const express = require("express");
const mongoose = require("mongoose");

const app = express();

mongoose.connect("mongodb://mongo:27017/testdb")
  .then(() => console.log("Mongo connected"))
  .catch(err => console.log(err));

app.get("/", (req, res) => {
  res.send("Backend running 🚀");
});

app.listen(3000, () => {
  console.log("Server on 3000");
});
