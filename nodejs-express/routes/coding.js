const express = require('express');

const codingController = require('../controllers/coding');
const isAuth = require("../middleware/is-auth");

const router = express.Router();

// GET /coding/logs
router.get('/logs', codingController.getLogs);

// POST /coding/log
router.post('/log', isAuth, codingController.postLog);

module.exports = router;