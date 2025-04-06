<template>
  <v-card flat>
    <v-card-title>Instructors</v-card-title>
    <v-card-text>
      <v-form>
        <v-text-field v-model="newInstructor.name" label="Name" dense />
        <v-btn color="primary" @click="handleAddInstructor">Add Instructor</v-btn>
      </v-form>

      <v-data-table
        :headers="headers"
        :items="instructors"
        item-value="id"
        dense
        class="mt-4"
      >
        <template #item.name="{ item }">
          <v-text-field v-model="item.name" @keyup.enter="handleUpdateInstructor(item)" dense hide-details />
        </template>
        <template #item.actions="{ item }">
          <v-btn icon @click="handleDeleteInstructor(item.id)">
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
  getInstructors,
  createInstructor,
  updateInstructor,
  deleteInstructor
} from '../../services/instructors'

const instructors = ref([])
const newInstructor = ref({ name: '' })

const headers = [
  { title: 'Name', value: 'name' },
  { title: 'Actions', value: 'actions', sortable: false }
]

onMounted(async () => {
  instructors.value = (await getInstructors()).data
})

const handleAddInstructor = async () => {
  await createInstructor(newInstructor.value)
  newInstructor.value = { name: '' }
  instructors.value = (await getInstructors()).data
}

const handleUpdateInstructor = async (item) => {
  await updateInstructor(item.id, item)
}

const handleDeleteInstructor = async (id) => {
  await deleteInstructor(id)
  instructors.value = (await getInstructors()).data
}
</script>

<style scoped>
.v-data-table {
  max-height: 400px;
  overflow-y: auto;
}
</style>
