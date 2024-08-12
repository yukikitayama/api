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

const learningSchema = new Schema(
  {
    startDate: { type: String, required: true },
    endDate: { type: String },
    name: { type: String, required: true },
    platform: { type: String, required: true },
    topic: { type: String, required: true },
  },
  { timestamps: true }
);

const concertSchema = new Schema(
  {
    date: { type: String, required: true },
    event: { type: String, required: true },
    artist: { type: String, required: true },
    organization: { type: String, required: true },
    location: { type: String, required: true },
  },
  { timestamps: true }
);

const practiceSchema = new Schema(
  {
    startDate: { type: String, required: true },
    endDate: { type: String },
    title: { type: String, required: true },
    composer: { type: String, required: true },
  },
  { timestamps: true }
);

const conn = mongoose.createConnection(`${process.env.MONGODB_SRV}/music`);

module.exports = {
  performance: conn.model("performances", performanceSchema),
  learning: conn.model("learnings", learningSchema),
  concert: conn.model("concerts", concertSchema),
  practice: conn.model("practices", practiceSchema),
};
