// server/controllers/coachController.js
const ZoomMeeting = require('../models/ZoomMeeting');

async function getAssignedMeetings(req, res) {
  const meetings = await ZoomMeeting.find({ coach: req.params.coachId });
  res.json(meetings);
}

async function joinMeeting(req, res) {
  const { meetingLink } = await ZoomMeeting.findById(req.body.meetingId);
  res.json({ meetingLink });
}

module.exports = { getAssignedMeetings, joinMeeting };
