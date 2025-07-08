// server/routes/coach.js
const router = require('express').Router();
const { getAssignedMeetings, joinMeeting } = require('../controllers/coachController');

router.get('/:coachId/meetings', getAssignedMeetings);
router.post('/:coachId/join', joinMeeting);

module.exports = router;
