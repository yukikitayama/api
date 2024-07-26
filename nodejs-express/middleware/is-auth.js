const jwt = require("jsonwebtoken");

module.exports = (req, res, next) => {
  const authHeader = req.get("Authorization");
  if (!authHeader) {
    const error = new Error("Not authenticated");
    error.statusCode = 401;
    throw error;
  }
  const token = authHeader.split(" ")[1];

  try {
    // verify() decodes and verifies
    decodedToken = jwt.verify(token, process.env.JWT_SIGN_SECRET);

  } catch (err) {
    err.statusCode = 500;
    throw err;
  }

  if (!decodedToken) {
    const error = new Error("Not authenticated");
    error.statusCode = 401;
    throw error;
  }

  // Store in request, so that we can use in other places
  req.userId = decodedToken.userId;

  next();
};