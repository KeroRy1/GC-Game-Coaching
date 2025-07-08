// server/utils/shopierWebhook.js

const Purchase = require('../models/Purchase');
const Coach    = require('../models/Coach');
const { sendWhatsAppMessage } = require('./whatsappNotifier');
const { createZoomMeeting }   = require('./zoom');

async function handle(req, res) {
  const { order_id, status } = req.body;
  if (status !== 'success') {
    return res.sendStatus(400);
  }

  // Satın alma kaydını güncelle
  const purchase = await Purchase.findById(order_id).populate('user');
  if (!purchase) {
    return res.sendStatus(404);
  }
  purchase.status = 'paid';
  await purchase.save();

  // Eşleşen koçları bul
  const coaches = await Coach.find({
    games: purchase.game,
    availableSlots: purchase.slot
  });

  if (!coaches.length) {
    console.warn('Uygun koç bulunamadı');
    return res.sendStatus(200);
  }

  // Rastgele bir koç seç
  const coach = coaches[Math.floor(Math.random() * coaches.length)];

  // Zoom toplantısı oluştur
  const meeting = await createZoomMeeting({
    user: purchase.user,
    coach,
    game: purchase.game,
    slot: purchase.slot
  });

  // WhatsApp bildirimi
  const message = `${purchase.game} ${purchase.slot} ${purchase.level}\nZoom Link: ${meeting.join_url}`;
  await sendWhatsAppMessage(coach.phoneNumber, message);

  res.sendStatus(200);
}

module.exports = { handle };
