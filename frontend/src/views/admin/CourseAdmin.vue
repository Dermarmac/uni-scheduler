<template>
  <div>
    <v-text-field v-model="course.name" label="Course Name" />
    <v-text-field v-model="course.code" label="Course Code" />
    <v-btn color="primary" @click="addCourse">Add Course</v-btn>

    <v-data-table :items="courses" :headers="headers" :search="search" dense fixed-header height="300">
      <template v-slot:top>
        <v-text-field v-model="search" label="Search Courses" />
      </template>
      <template v-slot:item.name="{ item }">
        <v-text-field v-model="item.name" @keyup.enter="updateCourse(item)" :rules="[v => !!v || 'Required']" />
      </template>
      <template v-slot:item.code="{ item }">
        <v-text-field v-model="item.code" @keyup.enter="updateCourse(item)" :rules="[v => !!v || 'Required']" />
      </template>
      <template v-slot:item.actions="{ item }">
        <v-btn @click="deleteCourse(item.id)" icon="mdi-delete" />
      </template>
    </v-data-table>

    <v-snackbar v-model="snackbar" :timeout="2000" color="success">
      {{ snackbarText }}
    </v-snackbar>
  </div>
</template>

<script>
import { getCourses, createCourse, updateCourse, deleteCourse } from '../services/courses'

export default {
  data() {
    return {
      course: { name: '', code: '' },
      courses: [],
      search: '',
      snackbar: false,
      snackbarText: '',
      headers: [
        { title: 'ID', value: 'id' },
        { title: 'Name', value: 'name' },
        { title: 'Code', value: 'code' },
        { title: 'Actions', value: 'actions', sortable: false },
      ]
    }
  },
  async mounted() {
    this.courses = (await getCourses()).data
  },
  methods: {
    async addCourse() {
      await createCourse(this.course)
      this.course = { name: '', code: '' }
      this.courses = (await getCourses()).data
    },
    async updateCourse(item) {
      await updateCourse(item.id, item)
      this.snackbarText = 'Course updated'
      this.snackbar = true
    },
    async deleteCourse(id) {
      await deleteCourse(id)
      this.courses = (await getCourses()).data
    }
  }
}
</script>
