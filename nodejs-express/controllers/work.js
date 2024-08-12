const Work = require("../models/work");

exports.getCertifications = (req, res, next) => {
  Work.certification
    .find()
    .sort({ date: "desc", name: "asc" })
    .then((certifications) => {
      res.status(200).json({
        certifications: certifications,
      });
    });
};

exports.getLearnings = (req, res, next) => {
  Work.learning
    .find()
    .sort({ startDate: "desc", name: "asc" })
    .then((learnings) => {
      res.status(200).json({
        learnings: learnings,
      });
    });
};

exports.getProjects = (req, res, next) => {
  Work.project
    .find()
    .sort({ startDate: "desc", name: "asc" })
    .then((projects) => {
      res.status(200).json({
        projects: projects,
      });
    });
};
