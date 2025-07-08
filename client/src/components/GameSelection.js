// client/src/components/GameSelection.js
import React, { useState } from 'react';
import PurchaseModal from './PurchaseModal';

const games = ['Apex','CS2','LoL','Valorant'];
const levels = ['Basit','Orta','Pro','Oyun Ustası'];
const slots = Array.from({ length: 12 }, (_,i)=>(`${8+i}:00`));

export default function GameSelection({ userId }) {
  const [modalOpen, setModalOpen] = useState(false);
  const [selection, setSelection] = useState({ game:'Apex', level:'Basit', slot:slots[0] });

  return (
    <div className="selection">
      <select onChange={e=>setSelection({...selection, game:e.target.value})}>
        {games.map(g=> <option key={g}>{g}</option>)}
      </select>
      <select onChange={e=>setSelection({...selection, level:e.target.value})}>
        {levels.map(l=> <option key={l}>{l}</option>)}
      </select>
      <select onChange={e=>setSelection({...selection, slot:e.target.value})}>
        {slots.map(s=> <option key={s}>{s}</option>)}
      </select>
      <button onClick={()=>setModalOpen(true)}>Satın Al</button>

      {modalOpen && (
        <PurchaseModal
          userId={userId}
          selection={selection}
          onClose={()=>setModalOpen(false)}
        />
      )}
    </div>
  );
}
