<template>
  <v-container>
    <v-row>
      <v-col>
        <h2>Class Schedule</h2>
        <v-btn color="primary" @click="fetchSchedule">Load Schedule</v-btn>
        <v-list>
          <v-list-item v-for="entry in schedule" :key="entry.course">
            <v-list-item-content>
              <v-list-item-title>
                {{ entry.course }} — {{ entry.instructor }} — {{ entry.room }} — {{ entry.timeslot }}
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import api from '../services/api';
import { getSchedule } from '../services/schedule';


export default {
  data() {
    return {
      schedule: [],
    };
  },
  methods: {
    async fetchSchedule() {
      const res = await api.getSchedule();
      this.schedule = res.data;
    },
  },
};
</script>
