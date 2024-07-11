const express = require("express");
const bodyParser = require("body-parser");

const codingRoutes = require("./routes/coding");

const app = express();

app.use(bodyParser.json()); // application/json

app.use((req, res, next) => {
  // Allow frontend client to sent request from any domain
  res.setHeader("Access-Control-Allow-Origin", "*");
  // Allow frontend client to request which method
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE");
  // Allow frontend client to attach which header to a request
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
  next();
});

app.use("/coding", codingRoutes);

app.listen(8080);
