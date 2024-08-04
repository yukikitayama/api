const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const performanceSchema = new Schema(
  {
    date: { type: String, required: true },
    title: { type: String, required: true },
    composer: { type: String, required: true },
    event: { type: String, required: true },
    location: { type: String, required: true },
  },
  {
    timestamps: true,
  }
);

const conn = mongoose.createConnection(`${process.env.MONGODB_SRV}/music`);
module.exports = conn.model("performances", performanceSchema);

