// server/routes/webhook.js
const router = require('express').Router();
const shopierWebhook = require('../utils/shopierWebhook');

router.post('/shopier', shopierWebhook.handle);

module.exports = router;
