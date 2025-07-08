// server/utils/zoom.js
console.log('[zoom stub] loaded from:', __filename);
async function createZoomMeeting({ user, coach, game, slot }) {
  return { join_url: 'https://zoom.us/j/0000000000' };
}
module.exports = { createZoomMeeting };
