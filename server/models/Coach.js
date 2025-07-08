// server/models/Coach.js

const mongoose = require('mongoose');

const coachSchema = new mongoose.Schema({
  user:   { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  games:           { type: [String], required: true },    // ['Valorant','LoL', …]
  availableSlots:  { type: [String], required: true },    // ['18:00','19:00', …]
  phoneNumber:     { type: String, required: true }       // 'whatsapp:+90…'
});

module.exports = mongoose.model('Coach', coachSchema);
