const Asset = require("../models/asset");

exports.getOverviews = (req, res, next) => {
  Asset.overview
    .find()
    .sort({ level: "asc" })
    .then((overviews) => {
      res.status(200).json({
        overviews: overviews,
      });
    });
};
