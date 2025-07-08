// sendBulkWhatsApp.js
// Bu script, tek dosyada bir veya birden fazla WhatsApp numarasına mesaj göndermenizi sağlar.

require('dotenv').config();  
const twilio = require('twilio')(  
  process.env.TWILIO_ACCOUNT_SID,  
  process.env.TWILIO_AUTH_TOKEN  
);

// 1) Gönderilecek numaralar
//    Dilediğiniz kadar “whatsapp:+90…” formatında numara ekleyin
const numbers = [
  'whatsapp:+905551112233',
  'whatsapp:+905556667778',
  'whatsapp:+905559991234'
];

// 2) Gönderilecek mesaj metni
const text = 'Seans detaylarınız ve Zoom linki aşağıdadır!';

(async () => {
  try {
    // Her numaraya paralel istek
    const sendJobs = numbers.map(to =>
      twilio.messages.create({
        from: process.env.WHATSAPP_FROM, // Örn: 'whatsapp:+90XXXXXXXXXX'
        to,
        body: text
      })
    );

    const results = await Promise.all(sendJobs);
    console.log('Mesaj gönderim sonuçları:', results);
  } catch (err) {
    console.error('WhatsApp mesajı gönderilirken hata:', err);
  }
})();
