<template>
  <v-app>
    <v-main>
      <Timetable />
      <Admin />
    </v-main>
  </v-app>
</template>

<script>
import Timetable from './views/Timetable.vue'
import Admin from './views/Admin.vue'

export default {
  components: {
    Timetable,
    Admin
  }
}
</script>
