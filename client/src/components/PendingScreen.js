// client/src/components/PendingScreen.js
import React, { useEffect, useState } from 'react';
import { getMeetings } from '../services/api';

export default function PendingScreen({ coachId }) {
  const [meetings, setMeetings] = useState([]);

  useEffect(() => {
    const iv = setInterval(async () => {
      const res = await getMeetings(coachId);
      setMeetings(res.data);
    }, 5000);
    return ()=> clearInterval(iv);
  }, [coachId]);

  if (!meetings.length) return <p>Link bekleniyor...</p>;
  return (
    <div>
      {meetings.map(m=>(
        <a key={m._id} href={m.meetingLink} target="_blank">Toplantıya Katıl</a>
      ))}
    </div>
  );
}
