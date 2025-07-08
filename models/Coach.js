// server/models/Coach.js
const mongoose = require('mongoose');

const coachSchema = new mongoose.Schema({
  user: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  availableSlots: [String]  // ["08:00","09:00",...]
});

module.exports = mongoose.model('Coach', coachSchema);
