const express = require("express");

const musicController = require("../controllers/music");
const isAuth = require("../middleware/is-auth");

const router = express.Router();

// GET /music/performances
router.get("/performances", musicController.getPerformances)

// POST /music/performance
router.post("/performance", isAuth, musicController.postPerformance);

module.exports = router;
