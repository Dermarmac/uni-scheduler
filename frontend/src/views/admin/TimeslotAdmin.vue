<template>
  <div>
    <v-text-field v-model="timeslot.day" label="Day" />
    <v-text-field v-model="timeslot.time" label="Time" />
    <v-btn color="primary" @click="addTimeslot">Add Timeslot</v-btn>

    <v-data-table :items="timeslots" :headers="headers" :search="search" dense fixed-header height="300">
      <template v-slot:top>
        <v-text-field v-model="search" label="Search Timeslots" />
      </template>
      <template v-slot:item.day="{ item }">
        <v-text-field v-model="item.day" @keyup.enter="updateTimeslot(item)" :rules="[v => !!v || 'Required']" />
      </template>
      <template v-slot:item.time="{ item }">
        <v-text-field v-model="item.time" @keyup.enter="updateTimeslot(item)" :rules="[v => !!v || 'Required']" />
      </template>
      <template v-slot:item.actions="{ item }">
        <v-btn @click="deleteTimeslot(item.id)" icon="mdi-delete" />
      </template>
    </v-data-table>

    <v-snackbar v-model="snackbar" :timeout="2000" color="success">
      {{ snackbarText }}
    </v-snackbar>
  </div>
</template>

<script>
import { getTimeslots, createTimeslot, updateTimeslot, deleteTimeslot } from '../services/timeslots'

export default {
  data() {
    return {
      timeslot: { day: '', time: '' },
      timeslots: [],
      search: '',
      snackbar: false,
      snackbarText: '',
      headers: [
        { title: 'ID', value: 'id' },
        { title: 'Day', value: 'day' },
        { title: 'Time', value: 'time' },
        { title: 'Actions', value: 'actions', sortable: false },
      ]
    }
  },
  async mounted() {
    this.timeslots = (await getTimeslots()).data
  },
  methods: {
    async addTimeslot() {
      await createTimeslot(this.timeslot)
      this.timeslot = { day: '', time: '' }
      this.timeslots = (await getTimeslots()).data
    },
    async updateTimeslot(item) {
      await updateTimeslot(item.id, item)
      this.snackbarText = 'Timeslot updated'
      this.snackbar = true
    },
    async deleteTimeslot(id) {
      await deleteTimeslot(id)
      this.timeslots = (await getTimeslots()).data
    }
  }
}
</script>
