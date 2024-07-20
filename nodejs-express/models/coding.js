const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const logSchema = new Schema(
  {
    date: { type: String, required: true },
    number: { type: String, required: true },
    level: { type: String, required: true },
    language: { type: String, required: true },
    title: { type: String, required: true },
    topics: { type: String, required: true },
    pickedFrom: { type: String, required: true },
    understanding: { type: Number },
    minuteSpent: { type: Number },
    firstTime: { type: Number },
    optimized: { type: Number },
    sawSolution: { type: Number },
    newReview: { type: Number },
    noEditorial: { type: Number },
    goodProblem: { type: Number },
    comment: { type: String },
    resource: { type: String },
  },
  { timestamps: true }
);

module.exports = mongoose.model("Log", logSchema);
