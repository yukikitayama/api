const Tennis = require("../models/tennis");

exports.getTournaments = (req, res, next) => {
  Tennis.tournament
    .find()
    .sort({ date: "desc" })
    .then((tournaments) => {
      res.status(200).json({
        tournaments: tournaments,
      });
    });
};
