import api from './api';

export function getInstructors() {
  return api.get('/instructors');
}

export function createInstructor(instructor) {
  return api.post('/instructors', instructor);
}

export function updateInstructor(id, instructor) {
  return api.put(`/instructors/${id}`, instructor);
}

export function deleteInstructor(id) {
  return api.delete(`/instructors/${id}`);
}
