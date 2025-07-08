// server/utils/emailNotifier.js
const nodemailer = require('nodemailer');

const transporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST,
  port: process.env.SMTP_PORT,
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS
  }
});

function sendUserEmail(userEmail, meetingLink) {
  const mailOptions = {
    from: process.env.SMTP_USER,
    to: userEmail,
    subject: 'Koçluk Toplantı Linkiniz',
    text: `Toplantınıza katılmak için tıklayın: ${meetingLink}`
  };
  return transporter.sendMail(mailOptions);
}

module.exports = { sendUserEmail };
