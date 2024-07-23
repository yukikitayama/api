const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const userSchema = new Schema({
  email: {
    type: String,
    required: true,
  },
  password: {
    type: String,
    required: true,
  },
  name: {
    tyope: String,
    required: true,
  },
});

// MongoDB collection
module.export = mongoose.model("user", userSchema);
