// server/routes/purchase.js
const router = require('express').Router();
const { initPurchase } = require('../controllers/purchaseController');

router.post('/', initPurchase);

module.exports = router;
