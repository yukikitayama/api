const express = require("express");

const workController = require("../controllers/work");

const router = express.Router();

// GET /work/certifications
router.get("/certifications", workController.getCertifications);

// GET /work/learnings
router.get("/learnings", workController.getLearnings);

module.exports = router;