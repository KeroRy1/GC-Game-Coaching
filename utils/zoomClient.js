// server/utils/zoomClient.js
const Zoom = require('zoomus')({
  key: process.env.ZOOM_API_KEY,
  secret: process.env.ZOOM_API_SECRET
});

async function createMeeting(slot) {
  const res = await Zoom.meeting.create({
    host_id: 'me',
    topic: `Game Coaching ${slot}`,
    type: 2,
    start_time: new Date(),
    duration: 60
  });
  return { meetingId: res.id, meetingLink: res.join_url };
}

module.exports = { createMeeting };
