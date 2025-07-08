// server/index.js
require('dotenv').config();
const express = require('express');
const mongoose = require('./utils/db');
const cors = require('cors');

const authRoutes = require('./routes/auth');
const purchaseRoutes = require('./routes/purchase');
const webhookRoutes = require('./routes/webhook');
const zoomRoutes = require('./routes/zoom');
const coachRoutes = require('./routes/coach');
const adminRoutes = require('./routes/admin');

const app = express();
app.use(cors());
app.use(express.json());

app.use('/api/auth', authRoutes);
app.use('/api/purchase', purchaseRoutes);
app.use('/api/webhook', webhookRoutes);
app.use('/api/zoom', zoomRoutes);
app.use('/api/coach', coachRoutes);
app.use('/api/admin', adminRoutes);

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
