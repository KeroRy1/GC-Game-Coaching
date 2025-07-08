// server/controllers/purchaseController.js
const Purchase = require('../models/Purchase');
const shopierWebhook = require('../utils/shopierWebhook');

async function initPurchase(req, res) {
  const { userId, game, level, slot } = req.body;
  const purchase = await Purchase.create({ user: userId, game, level, slot });
  // Shopier ödeme linki üret
  const paymentUrl = shopierWebhook.generateLink(purchase._id, game, level, slot);
  res.json({ paymentUrl });
}

module.exports = { initPurchase };
