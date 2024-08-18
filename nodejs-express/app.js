const express = require("express");
const bodyParser = require("body-parser");
const mongoose = require("mongoose");
require("dotenv").config();

const mongodbSrv = process.env.MONGODB_SRV;

const codingRoutes = require("./routes/coding");
const authRoutes = require("./routes/auth");
const musicRoutes = require("./routes/music");
const workRoutes = require("./routes/work");
const tennisRoutes = require("./routes/tennis");
const assetRoutes = require("./routes/asset");

const app = express();

app.use(bodyParser.json()); // application/json

app.use((req, res, next) => {
  // Allow frontend client to sent request from any domain
  res.setHeader("Access-Control-Allow-Origin", "*");
  // Allow frontend client to request which method
  res.setHeader(
    "Access-Control-Allow-Methods",
    "GET, POST, PUT, PATCH, DELETE"
  );
  // Allow frontend client to attach which header to a request
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
  next();
});

app.use("/coding", codingRoutes);
app.use("/auth", authRoutes);
app.use("/music", musicRoutes);
app.use("/work", workRoutes);
app.use("/tennis", tennisRoutes);
app.use("/asset", assetRoutes);

mongoose
  .connect(mongodbSrv)
  .then((result) => {
    app.listen(8080);
  })
  .catch((err) => console.log(err));
