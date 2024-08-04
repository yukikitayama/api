const Music = require("../models/music");

exports.getPerformances = (req, res, next) => {
  Music.find()
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
  const performance = new Music(req.body);

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
