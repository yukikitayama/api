const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const tournamentSchema = new Schema(
  {
    date: { type: String, required: true },
    name: { type: String, required: true },
    location: { type: String },
    format: { type: String },
    level: { type: String },
    result: { type: String },
    comment: { type: String },
  },
  { timestamps: true }
);

const conn = mongoose.createConnection(`${process.env.MONGODB_SRV}/tennis`);

module.exports = {
  tournament: conn.model("tournaments", tournamentSchema),
};
