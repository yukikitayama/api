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
    type: String,
    required: true,
  },
});

// MongoDB collection
// module.exports = mongoose.model("user", userSchema);

const conn = mongoose.createConnection(
  `${process.env.MONGODB_SRV}/authentication`
);
module.exports = conn.model("user", userSchema);
