<template>
  <div>
    <v-text-field v-model="instructor.name" label="Instructor Name" />
    <v-btn color="primary" @click="addInstructor">Add Instructor</v-btn>

    <v-data-table :items="instructors" :headers="headers" :search="search" dense fixed-header height="300">
      <template v-slot:top>
        <v-text-field v-model="search" label="Search Instructors" />
      </template>
      <template v-slot:item.name="{ item }">
        <v-text-field v-model="item.name" @keyup.enter="updateInstructor(item)" :rules="[v => !!v || 'Required']" />
      </template>
      <template v-slot:item.actions="{ item }">
        <v-btn @click="deleteInstructor(item.id)" icon="mdi-delete" />
      </template>
    </v-data-table>

    <v-snackbar v-model="snackbar" :timeout="2000" color="success">
      {{ snackbarText }}
    </v-snackbar>
  </div>
</template>

<script>
import { getInstructors, createInstructor, updateInstructor, deleteInstructor } from '../services/instructors'

export default {
  data() {
    return {
      instructor: { name: '' },
      instructors: [],
      search: '',
      snackbar: false,
      snackbarText: '',
      headers: [
        { title: 'ID', value: 'id' },
        { title: 'Name', value: 'name' },
        { title: 'Actions', value: 'actions', sortable: false },
      ]
    }
  },
  async mounted() {
    this.instructors = (await getInstructors()).data
  },
  methods: {
    async addInstructor() {
      await createInstructor(this.instructor)
      this.instructor = { name: '' }
      this.instructors = (await getInstructors()).data
    },
    async updateInstructor(item) {
      await updateInstructor(item.id, item)
      this.snackbarText = 'Instructor updated'
      this.snackbar = true
    },
    async deleteInstructor(id) {
      await deleteInstructor(id)
      this.instructors = (await getInstructors()).data
    }
  }
}
</script>
