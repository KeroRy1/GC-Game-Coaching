// server/models/ZoomMeeting.js
const mongoose = require('mongoose');

const zoomMeetingSchema = new mongoose.Schema({
  meetingId: String,
  meetingLink: String,
  coach: { type: mongoose.Schema.Types.ObjectId, ref: 'Coach' },
  slot: String
});

module.exports = mongoose.model('ZoomMeeting', zoomMeetingSchema);
