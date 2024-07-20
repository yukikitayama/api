const Log = require("../models/coding");

exports.getLogs = (req, res, next) => {
  Log.find()
    .then((logs) => {
      res.status(200).json({ logs: logs });
    })
    .catch((err) => {
      console.log(err);
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
