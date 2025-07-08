// client/src/services/api.js
import axios from 'axios';

const API = axios.create({ baseURL: 'http://localhost:5000/api' });

export const initPurchase = data => API.post('/purchase', data);
export const getMeetings = coachId => API.get(`/coach/${coachId}/meetings`);
export const joinMeeting = (coachId, meetingId) => API.post(`/coach/${coachId}/join`, { meetingId });
