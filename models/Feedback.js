// server/models/Feedback.js
const mongoose = require('mongoose');

const feedbackSchema = new mongoose.Schema({
  purchase: { type: mongoose.Schema.Types.ObjectId, ref: 'Purchase' },
  rating: Number,
  comment: String
});

module.exports = mongoose.model('Feedback', feedbackSchema);
