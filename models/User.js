// server/models/User.js
const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  email: String,
  passwordHash: String,
  role: { type: String, enum: ['user','coach','admin'], default: 'user' }
});

module.exports = mongoose.model('User', userSchema);
