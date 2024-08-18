const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const overviewSchema = new Schema(
  {
    content: { type: String, required: true },
    level: { type: Number },
  },
  { timestamps: true }
);

const conn = mongoose.createConnection(`${process.env.MONGODB_SRV}/asset`);

module.exports = {
  overview: conn.model("overviews", overviewSchema),
};
