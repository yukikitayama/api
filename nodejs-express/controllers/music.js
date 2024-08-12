const Music = require("../models/music");

exports.getPerformances = (req, res, next) => {
  Music.performance.find()
    .sort({ date: "desc", title: "asc" })
    .then((performances) => {
      res.status(200).json({
        performances: performances,
      });
    })
    .catch((err) => {
      if (!err.statusCode) {
        err.statusCode = 500;
      }
      next(err);
    });
};

exports.postPerformance = (req, res, next) => {
  const performance = new Music.performance(req.body);

  performance
    .save()
    .then((result) => {
      res.status(201).json({
        message: "Performance uploaded successfully",
      });
    })
    .catch((err) => {
      console.log(err);
    });
};

exports.getLearnings = (req, res, next) => {
  Music.learning
    .find()
    .sort({ startDate: "desc", name: "asc" })
    .then((learnings) => {
      res.status(200).json({
        learnings: learnings,
      });
    });
};

exports.getConcerts = (req, res, next) => {
  Music.concert
    .find()
    .sort({ date: "desc" })
    .then((concerts) => {
      res.status(200).json({
        concerts: concerts,
      });
    });
};

exports.getPractices = (req, res, next) => {
  Music.practice
    .find()
    .sort({ startDate: "desc", title: "asc" })
    .then((practices) => {
      res.status(200).json({
        practices: practices,
      });
    });
};