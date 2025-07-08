// client/src/components/PurchaseModal.js
import React, { useState } from 'react';
import { initPurchase } from '../services/api';

export default function PurchaseModal({ userId, selection, onClose }) {
  const [paymentUrl, setPaymentUrl] = useState('');

  const handlePay = async () => {
    const res = await initPurchase({ userId, ...selection });
    window.location.href = res.data.paymentUrl;
  };

  return (
    <div className="modal">
      <h2>Onayla</h2>
      <p>Oyun: {selection.game}</p>
      <p>Seviye: {selection.level}</p>
      <p>Saat: {selection.slot}</p>
      <button onClick={handlePay}>Ödeme Yap</button>
      <button onClick={onClose}>İptal</button>
    </div>
  );
}
