import api from './api';

export function getSchedule() {
  return api.get('/schedule');
}

export function generateSchedule() {
  return api.post('/generate');
}

export function setConstraints(data) {
  return api.post('/constraints', data);
}

export function uploadFile(file) {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/upload', formData);
}
