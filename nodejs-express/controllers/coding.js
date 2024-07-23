const Log = require("../models/coding");

exports.getLogs = (req, res, next) => {
  // Pagination
  // Set 1 as default
  const currentPage = req.query.page || 1;
  const perPage = 10;

  let totalItems;
  Log.find()
    .countDocuments()
    .then((count) => {
      totalItems = count;
      return Log.find()
        .skip((currentPage - 1) * perPage)
        .limit(perPage);
    })
    .then((logs) => {
      res.status(200).json({ logs: logs, totalItems: totalItems });
    })
    .catch((err) => {
      if (!err.statusCode) {
        err.statusCode = 500;
      }
      next(err);
    });
};

exports.postLog = (req, res, next) => {
  // console.log(req.body);

  // Save log in MongoDB
  const log = new Log(req.body);
  log
    .save()
    .then((result) => {
      // console.log(result);
      res.status(201).json({
        message: "Log created successfully",
        log: result,
      });
    })
    .catch((err) => {
      console.log(err);
    });
};
