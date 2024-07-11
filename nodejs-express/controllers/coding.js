const logs = [{ _id: "1", title: "title1", date: new Date() }];

exports.getLogs = (req, res, next) => {
  res.status(200).json({ logs: logs });
};

exports.postLog = (req, res, next) => {
  // body field is added by body-parser
  const title = req.body.title;
  // Create log in db
  res.status(201).json({
    message: "Log created successfully",
    log: { id: new Date().toISOString(), title: title },
  });
};
