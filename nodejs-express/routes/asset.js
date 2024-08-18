const express = require("express");

const assetController = require("../controllers/asset");
const isAuth = require("../middleware/is-auth");

const router = express.Router();

// GET /asset/overviews
router.get("/overviews", isAuth, assetController.getOverviews);

module.exports = router;