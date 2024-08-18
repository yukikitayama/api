const express = require("express");

const tennisController = require("../controllers/tennis");

const router = express.Router();

// GET /tennis/tournaments
router.get("/tournaments", tennisController.getTournaments);

module.exports = router;