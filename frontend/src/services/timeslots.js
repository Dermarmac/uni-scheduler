import api from './api';

export function getTimeslots() {
  return api.get('/timeslots');
}

export function createTimeslot(timeslot) {
  return api.post('/timeslots', timeslot);
}

export function updateTimeslot(id, timeslot) {
  return api.put(`/timeslots/${id}`, timeslot);
}

export function deleteTimeslot(id) {
  return api.delete(`/timeslots/${id}`);
}
