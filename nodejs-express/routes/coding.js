const express = require('express');

const codingController = require('../controllers/coding');

const router = express.Router();

// GET /coding/logs
router.get('/logs', codingController.getLogs);

// POST /coding/log
router.post('/post', codingController.postLog);

module.exports = router;