// server/utils/shopierWebhook.js

const Purchase = require('../models/Purchase');
const Coach    = require('../models/Coach');
const { sendWhatsAppMessage } = require('./whatsappNotifier');
const { createZoomMeeting }   = require('./zoom');

/**
 * Shopier’den gelen ödeme webhook’unu işler:
 * 1. Ödeme başarılıysa purchase kaydını günceller.
 * 2. Uygun koç(lar)ı bulur.
 * 3. Zoom toplantısı oluşturur.
 * 4. Tüm koçlara WhatsApp bildirimi gönderir.
 */
async function handle(req, res) {
  try {
    const { order_id, status } = req.body;

    // Sadece başarısız olmayan ödemeleri işle
    if (status !== 'success') {
      return res.status(400).json({ error: 'Invalid payment status' });
    }

    // Satın alma kaydını bul ve kullanıcıyı populate et
    const purchase = await Purchase.findById(order_id).populate('user');
    if (!purchase) {
      return res.status(404).json({ error: 'Purchase not found' });
    }

    // Durumu güncelle
    purchase.status = 'paid';
    await purchase.save();

    // İstenen oyun ve slot’a uygun koçları çek
    const coaches = await Coach.find({
      games: purchase.game,
      availableSlots: purchase.slot
    });

    if (!coaches.length) {
      console.warn('Uygun koç bulunamadı:', purchase.game, purchase.slot);
      return res.status(200).json({ warning: 'No coaches available' });
    }

    // Tüm koçların WhatsApp numaralarını al
    const numbers = coaches.map(c => c.phoneNumber);

    // Zoom toplantısını ilk koç için oluştur (koç başına ayrı toplantı gerekirse döngüye alabilirsin)
    const meeting = await createZoomMeeting({
      user:  purchase.user,
      coach: coaches[0],
      game:  purchase.game,
      slot:  purchase.slot
    });

    // Gönderilecek mesaj metni
    const text = 
      `${purchase.game} seansınız ${purchase.slot} tarihinde onaylandı.\n` +
      `Seviye: ${purchase.level}\n` +
      `Zoom link: ${meeting.join_url}`;

    // WhatsApp üzerinden tüm koçlara bildir
    const results = await sendWhatsAppMessage(numbers, text);

    return res.status(200).json({
      message: 'Webhook processed, WhatsApp notifications sent',
      twilio: results
    });

  } catch (err) {
    console.error('shopierWebhook error:', err);
    return res.status(500).json({ error: err.message });
  }
}

module.exports = { handle };
