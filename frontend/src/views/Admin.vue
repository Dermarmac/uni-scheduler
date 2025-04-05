<template>
  <v-container>
    <v-tabs v-model="tab" color="primary" grow>
      <v-tab><v-icon left>mdi-book</v-icon>Courses</v-tab>
      <v-tab><v-icon left>mdi-account</v-icon>Instructors</v-tab>
      <v-tab><v-icon left>mdi-calendar-clock</v-icon>Timeslots</v-tab>
    </v-tabs>

    <v-tabs-items v-model="tab" class="transition-fade" style="transition: opacity 0.5s ease-in-out;">
      <v-tab-item>
        <component :is="currentComponent" />
      </v-tab-item>
    </v-tabs-items>
  </v-container>
</template>

<script setup>
import { ref, computed, defineAsyncComponent } from 'vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const tab = ref(0)

const components = [
  defineAsyncComponent({
    loader: () => import('./admin/CourseAdmin.vue'),
    loadingComponent: LoadingSpinner,
    delay: 200
  }),
  defineAsyncComponent({
    loader: () => import('./admin/InstructorAdmin.vue'),
    loadingComponent: LoadingSpinner,
    delay: 200
  }),
  defineAsyncComponent({
    loader: () => import('./admin/TimeslotAdmin.vue'),
    loadingComponent: LoadingSpinner,
    delay: 200
  })
]

const currentComponent = computed(() => components[tab.value])
</script>
