const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const certificationSchema = new Schema(
  {
    date: { type: String, required: true },
    name: { type: String, required: true },
    organization: { type: String, required: true },
    skill: { type: String, required: true },
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
  {
    timestamps: true,
  }
);

const projectSchema = new Schema(
  {
    startDate: { type: String, required: true },
    endDate: { type: String },
    name: { type: String, required: true },
    skill: { type: String, required: true },
  },
  {
    timestamps: true,
  }
);

const conn = mongoose.createConnection(`${process.env.MONGODB_SRV}/work`);

module.exports = {
  certification: conn.model("certifications", certificationSchema),
  learning: conn.model("learnings", learningSchema),
  project: conn.model("projects", projectSchema),
};
