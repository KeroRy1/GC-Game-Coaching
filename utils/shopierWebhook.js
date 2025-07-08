// server/utils/shopierWebhook.js
const Purchase = require('../models/Purchase');
const ZoomMeeting = require('../models/ZoomMeeting');
const { createMeeting } = require('./zoomClient');
const { sendCoachNotification } = require('./whatsappNotifier');
const { sendUserEmail } = require('./emailNotifier');
const Coach = require('../models/Coach');

function generateLink(id, game, level, slot) {
  // Shopier’a redirect edecek linki oluştur
  return `https://www.shopier.com/integration/pay?api_key=${process.env.SHOPIER_API_KEY}&order_id=${id}`;
}

async function handle(req, res) {
  const { order_id, status } = req.body;
  if (status !== 'success') return res.sendStatus(400);

  const purchase = await Purchase.findById(order_id);
  purchase.status = 'paid';

  // Rastgele müsait koç seç
  const coaches = await Coach.find({ availableSlots: purchase.slot });
  const coach = coaches[Math.floor(Math.random()*coaches.length)];

  // Zoom toplantısı oluştur
  const { meetingId, meetingLink } = await createMeeting(purchase.slot);
  const zm = await ZoomMeeting.create({ meetingId, meetingLink, coach, slot: purchase.slot });
  purchase.zoomMeeting = zm._id;
  await purchase.save();

  // Koça WhatsApp bildirimi
  await sendCoachNotification(purchase);

  // Kullanıcıya e-posta bildirimi
  const user = await purchase.populate('user').execPopulate();
  await sendUserEmail(user.email, meetingLink);

  res.sendStatus(200);
}

module.exports = { generateLink, handle };
