// server/models/Purchase.js
const mongoose = require('mongoose');

const purchaseSchema = new mongoose.Schema({
  user: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  game: String,
  level: String,
  slot: String,
  status: { type: String, enum: ['pending','paid'], default: 'pending' },
  zoomMeeting: { type: mongoose.Schema.Types.ObjectId, ref: 'ZoomMeeting' },
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Purchase', purchaseSchema);
