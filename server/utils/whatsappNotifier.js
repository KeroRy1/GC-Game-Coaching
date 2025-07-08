// server/utils/whatsappNotifier.js

require('dotenv').config();  
const twilio = require('twilio')(
  process.env.TWILIO_ACCOUNT_SID,
  process.env.TWILIO_AUTH_TOKEN
);

/**
 * Bir veya birden fazla WhatsApp numarasına mesaj gönderir.
 *
 * @param {string|string[]} to      Tekil veya dizi halinde “whatsapp:+90…” formatlı numaralar
 * @param {string}         message Gönderilecek metin
 * @returns {Promise<Object[]>}    Twilio’dan gelen yanıtların listesi
 */
async function sendWhatsAppMessage(to, message) {
  const recipients = Array.isArray(to) ? to : [to];
  const sendPromises = recipients.map(number =>
    twilio.messages.create({
      from: process.env.WHATSAPP_FROM,  // Örn: 'whatsapp:+90XXXXXXXXXX'
      to: number,
      body: message
    })
  );
  return Promise.all(sendPromises);
}

// ————————————————————————————————————————————————
// Aşağıya istediğin numaraları ve metni ekle:
// ————————————————————————————————————————————————

const numbers = [
  'whatsapp:+905551112233',
  'whatsapp:+905556667778',
  'whatsapp:+905559991234'
];

const text = 'Seans detaylarınız ve Zoom linki aşağıdadır!';

// Otomatik çalıştırma: dosya require edildiğinde değil, script doğrudan çalıştırıldığında
if (require.main === module) {
  (async () => {
    try {
      const results = await sendWhatsAppMessage(numbers, text);
      console.log('Mesaj gönderim sonuçları:', results);
    } catch (err) {
      console.error('WhatsApp gönderim hatası:', err);
    }
  })();
}

module.exports = { sendWhatsAppMessage };
