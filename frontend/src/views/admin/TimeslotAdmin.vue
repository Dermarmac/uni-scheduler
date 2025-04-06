<template>
  <v-card flat>
    <v-card-title>Timeslots</v-card-title>
    <v-card-text>
      <v-form>
        <v-text-field v-model="newTimeslot.day" label="Day" dense />
        <v-text-field v-model="newTimeslot.time" label="Time" dense />
        <v-btn color="primary" @click="handleAddTimeslot">Add Timeslot</v-btn>
      </v-form>

      <v-data-table
        :headers="headers"
        :items="timeslots"
        item-value="id"
        dense
        class="mt-4"
      >
        <template #item.day="{ item }">
          <v-text-field v-model="item.day" @keyup.enter="handleUpdateTimeslot(item)" dense hide-details />
        </template>
        <template #item.time="{ item }">
          <v-text-field v-model="item.time" @keyup.enter="handleUpdateTimeslot(item)" dense hide-details />
        </template>
        <template #item.actions="{ item }">
          <v-btn icon @click="handleDeleteTimeslot(item.id)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {
  getTimeslots,
  createTimeslot,
  updateTimeslot,
  deleteTimeslot
} from '../../services/timeslots'

const timeslots = ref([])
const newTimeslot = ref({ day: '', time: '' })

const headers = [
  { title: 'Day', value: 'day' },
  { title: 'Time', value: 'time' },
  { title: 'Actions', value: 'actions', sortable: false }
]

onMounted(async () => {
  timeslots.value = (await getTimeslots()).data
})

const handleAddTimeslot = async () => {
  await createTimeslot(newTimeslot.value)
  newTimeslot.value = { day: '', time: '' }
  timeslots.value = (await getTimeslots()).data
}

const handleUpdateTimeslot = async (item) => {
  await updateTimeslot(item.id, item)
}

const handleDeleteTimeslot = async (id) => {
  await deleteTimeslot(id)
  timeslots.value = (await getTimeslots()).data
}
</script>

<style scoped>
.v-data-table {
  max-height: 400px;
  overflow-y: auto;
}
</style>
