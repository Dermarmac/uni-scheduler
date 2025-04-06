<template>
  <v-card flat>
    <v-card-title>Courses</v-card-title>
    <v-card-text>
      <v-form>
        <v-text-field v-model="newCourse.name" label="Name" dense />
        <v-text-field v-model="newCourse.code" label="Code" dense />
        <v-btn color="primary" @click="handleAddCourse">Add Course</v-btn>
      </v-form>

      <v-data-table
        :headers="headers"
        :items="courses"
        item-value="id"
        dense
        class="mt-4"
      >
        <template #item.name="{ item }">
          <v-text-field v-model="item.name" @keyup.enter="handleUpdateCourse(item)" dense hide-details />
        </template>
        <template #item.code="{ item }">
          <v-text-field v-model="item.code" @keyup.enter="handleUpdateCourse(item)" dense hide-details />
        </template>
        <template #item.actions="{ item }">
          <v-btn icon @click="handleDeleteCourse(item.id)">
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
  getCourses,
  createCourse,
  updateCourse,
  deleteCourse
} from '../../services/courses'

const courses = ref([])
const newCourse = ref({ name: '', code: '' })

const headers = [
  { title: 'Name', value: 'name' },
  { title: 'Code', value: 'code' },
  { title: 'Actions', value: 'actions', sortable: false }
]

onMounted(async () => {
  courses.value = (await getCourses()).data
})

const handleAddCourse = async () => {
  await createCourse(newCourse.value)
  newCourse.value = { name: '', code: '' }
  courses.value = (await getCourses()).data
}

const handleUpdateCourse = async (item) => {
  await updateCourse(item.id, item)
}

const handleDeleteCourse = async (id) => {
  await deleteCourse(id)
  courses.value = (await getCourses()).data
}
</script>

<style scoped>
.v-data-table {
  max-height: 400px;
  overflow-y: auto;
}
</style>
