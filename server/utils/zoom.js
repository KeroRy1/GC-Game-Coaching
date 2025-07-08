// server/utils/zoom.js

/**
 * Basit bir stub: gerçek Zoom API entegrasyonu yoksa
 * join_url olarak sabit bir link döner.
 *
 * @param {Object} options
 * @param {Object} options.user  Kullanıcı objesi (Magento’da user)
 * @param {Object} options.coach Koç objesi
 * @param {string} options.game  Oyun adı
 * @param {string} options.slot  Seans saati
 *
 * @returns {Promise<{ join_url: string }>}
 */
async function createZoomMeeting({ user, coach, game, slot }) {
  // Eğer gerçek entegrasyon istiyorsan, burada Zoom JWT ile istek atabilirsin.
  // Şimdilik username is required hatasını önlemek için stub:
  return {
    join_url: 'https://zoom.us/j/1234567890?pwd=stubpassword'
  };
}

module.exports = { createZoomMeeting };
