// server/index.js

require('dotenv').config();               // .env dosyasını yükle
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const { handle: shopierWebhookHandler } = require('./utils/shopierWebhook');

const app = express();

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// MongoDB bağlantısı
mongoose
  .connect(process.env.MONGODB_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true
  })
  .then(() => console.log('MongoDB bağlantısı başarılı'))
  .catch(err => console.error('MongoDB bağlantı hatası:', err));

// Sağlık kontrolü endpoint’i
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

// Shopier webhook endpoint’i
app.post('/api/webhook/shopier', shopierWebhookHandler);

// Port’u dinle
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Sunucu ${PORT} portunda çalışıyor`);
});
