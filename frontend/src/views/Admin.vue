// Updated Admin.vue with tabbed layout for CRUD operations
<template>
  <v-container>
  <v-dialog v-model="invalidDialog" max-width="800">
    <v-card>
      <v-card-title class="text-h6">Invalid Rows Skipped</v-card-title>
      <v-card-text>
        <v-data-table :items="invalidRows" :headers="invalidHeaders" class="elevation-1" dense>
          <template v-slot:item.raw="{ item }">
            <v-text-field
              v-model="item.raw"
              :error="!isValidJSON(item.raw)"
              @keyup.enter="updateInvalidRow(item)"
            />
          </template>
          <template v-slot:item.reason="{ item }">
            <span v-if="!isValidJSON(item.raw)" class="text-red">Invalid JSON or missing fields</span>
            <span v-else class="text-green">Valid</span>
          </template>
        </v-data-table>
        <v-btn color="primary" @click="reapplyInvalidRows">Reapply Validated Rows</v-btn>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" text @click="invalidDialog = false">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <v-btn @click="saveAllChanges" class="mb-3 mr-2" color="success">
    <v-icon left>mdi-content-save</v-icon>Save All Changes
  </v-btn>
  <v-btn @click="exportData" class="mb-3 mr-2" color="info">
    <v-icon left>mdi-file-export</v-icon>Export CSV
  </v-btn>
  <v-btn @click="undoLastChange" class="mb-3 mr-2" color="secondary">
  
<v-btn @click="triggerFileInput" class="mb-3" color="warning">
  <v-icon left>mdi-file-upload</v-icon>Import Excel
</v-btn>
<input ref="fileInput" type="file" accept=".xlsx" @change="importExcel" style="display: none" />
    <v-icon left>mdi-undo</v-icon>Undo Last Change
  </v-btn>
  <v-snackbar v-model="snackbar" :timeout="2000" color="success">
    {{ snackbarText }}
  </v-snackbar>
  <v-snackbar v-model="successDialog" :timeout="3000" color="info">
    Revalidated rows added: {{ revalidateSuccess }}, Skipped again: {{ revalidateFailure }}
  </v-snackbar>
    <v-tabs v-model="tab" color="primary" grow>
      <v-tab><v-icon left>mdi-book</v-icon>Courses</v-tab>
      <v-tab><v-icon left>mdi-account</v-icon>Instructors</v-tab>
      <v-tab><v-icon left>mdi-calendar-clock</v-icon>Timeslots</v-tab>
    </v-tabs>

    <v-tabs-items v-model="tab" class="transition-fade" style="transition: opacity 0.5s ease-in-out;">
      <!-- Courses Tab -->
      <v-tab-item>
        <v-text-field v-model="course.name" label="Course Name" />
        <v-text-field v-model="course.code" label="Course Code" />
        <v-btn color="primary" @click="addCourse">Add Course</v-btn>

        <v-data-table :items="courses" :headers="courseHeaders" :search="search" dense fixed-header height="300">
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
      </v-tab-item>

      <!-- Instructors Tab -->
      <v-tab-item>
        <v-text-field v-model="instructor.name" label="Instructor Name" />
        <v-btn color="primary" @click="addInstructor">Add Instructor</v-btn>

        <v-data-table :items="instructors" :headers="instructorHeaders" :search="search" dense fixed-header height="300">
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
      </v-tab-item>

      <!-- Timeslots Tab -->
      <v-tab-item>
        <v-text-field v-model="timeslot.day" label="Day" />
        <v-text-field v-model="timeslot.time" label="Time" />
        <v-btn color="primary" @click="addTimeslot">Add Timeslot</v-btn>

        <v-data-table :items="timeslots" :headers="timeslotHeaders" :search="search" dense fixed-header height="300">
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
      </v-tab-item>
    </v-tabs-items>
  </v-container>
</template>

<script>
import {
  getCourses, createCourse, updateCourse, deleteCourse
} from '../services/courses'
import {
  getInstructors, createInstructor, updateInstructor, deleteInstructor
} from '../services/instructors'
import {
  getTimeslots, createTimeslot, updateTimeslot, deleteTimeslot
} from '../services/timeslots'

export default {
  data() {
    return {
      tab: 0,
      search: '',
      // Course data
      course: { name: '', code: '' },
      courses: [],
      courseHeaders: [
        { title: 'ID', value: 'id' },
        { title: 'Name', value: 'name' },
        { title: 'Code', value: 'code' },
        { title: 'Actions', value: 'actions', sortable: false },
      ],
      // Instructor data
      instructor: { name: '' },
      instructors: [],
      snackbar: false,
      snackbarText: '',
      unsavedChanges: new Set(),
      undoStack: [],
      successDialog: false,
      revalidateSuccess: 0,
      revalidateFailure: 0,
      invalidDialog: false,
      invalidRows: [],
      invalidHeaders: [
        { title: 'Row #', value: 'row' },
        { title: 'Row Data', value: 'raw' },
        { title: 'Reason', value: 'reason' }
      ],
      instructorHeaders: [
        { title: 'ID', value: 'id' },
        { title: 'Name', value: 'name' },
        { title: 'Actions', value: 'actions', sortable: false },
      ],
      // Timeslot data
      timeslot: { day: '', time: '' },
      timeslots: [],
      timeslotHeaders: [
        { title: 'ID', value: 'id' },
        { title: 'Day', value: 'day' },
        { title: 'Time', value: 'time' },
        { title: 'Actions', value: 'actions', sortable: false },
      ]
    }
  },
      // Course data
      course: { name: '', code: '' },
      courses: [],
      courseHeaders: [
        { title: 'ID', value: 'id' },
        { title: 'Name', value: 'name' },
        { title: 'Code', value: 'code' },
        { title: 'Actions', value: 'actions', sortable: false },
      ],
      // Instructor data
      instructor: { name: '' },
      instructors: [],
      snackbar: false,
      snackbarText: '',
      unsavedChanges: new Set(),
      undoStack: [],
      successDialog: false,
      revalidateSuccess,
      revalidateFailure,
      invalidDialog: false,
      invalidRows: [],
      invalidHeaders: [
        { title: 'Row #', value: 'row' },
        { title: 'Row Data', value: 'raw' },
        { title: 'Reason', value: 'reason' }
      ],
      instructorHeaders: [
        { title: 'ID', value: 'id' },
        { title: 'Name', value: 'name' },
        { title: 'Actions', value: 'actions', sortable: false },
      ],
      // Timeslot data
      timeslot: { day: '', time: '' },
      timeslots: [],
      timeslotHeaders: [
        { title: 'ID', value: 'id' },
        { title: 'Day', value: 'day' },
        { title: 'Time', value: 'time' },
        { title: 'Actions', value: 'actions', sortable: false },
      ]
    }
  ,
  async mounted() {
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        const inputs = Array.from(document.querySelectorAll('input'));
        const index = inputs.indexOf(document.activeElement);
        if (index !== -1 && inputs[index + 1]) {
          inputs[index + 1].focus();
          e.preventDefault();
        }
      }
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'z') {
        e.preventDefault();
        this.undoLastChange();
      }
    });
    this.courses = (await getCourses()).data
    this.instructors = (await getInstructors()).data
    this.timeslots = (await getTimeslots()).data
  },
  methods: {
    updateInvalidRow(item) {
      if (this.isValidJSON(item.raw)) {
        const parsed = JSON.parse(item.raw);
        if (this.tab === 0) this.courses.push(parsed);
        else if (this.tab === 1) this.instructors.push(parsed);
        else this.timeslots.push(parsed);

        this.snackbarText = 'Row successfully reapplied';
        this.snackbar = true;

        this.invalidRows = this.invalidRows.filter(r => r !== item);
        if (this.invalidRows.length === 0) {
          this.invalidDialog = false;
        }
      }
    },
    isValidJSON(text) {
      try {
        const obj = JSON.parse(text);
        if (this.tab === 0) return obj.name && obj.code;
        if (this.tab === 1) return obj.name;
        if (this.tab === 2) return obj.day && obj.time;
        return false;
      } catch (e) {
        return false;
      }
    },
    reapplyInvalidRows() {
      const parsed = this.invalidRows.map(row => {
        try {
          return JSON.parse(row.raw);
        } catch (e) {
          return null;
        }
      }).filter(r => r);

      const isValidRow = (row) => {
        if (this.tab === 0) return row.name && row.code;
        if (this.tab === 1) return row.name;
        if (this.tab === 2) return row.day && row.time;
        return false;
      };

      const valid = parsed.filter(isValidRow);

      if (this.tab === 0) this.courses.push(...valid);
      else if (this.tab === 1) this.instructors.push(...valid);
      else this.timeslots.push(...valid);

      this.snackbarText = `${valid.length} revalidated row(s) added`;
      this.snackbar = true;
      const remainingInvalids = this.invalidRows.filter(row => !this.isValidJSON(row.raw));
      if (remainingInvalids.length === 0) {
        this.invalidDialog = false;
      }
      this.invalidRows = [];
    },
    triggerFileInput() {
      this.$refs.fileInput.click()
    },

    async importExcel(event) {
      const file = event.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = async (e) => {
        const data = new Uint8Array(e.target.result);
        const XLSX = await import('xlsx');
        const workbook = XLSX.read(data, { type: 'array' });
        const sheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[sheetName];
        const jsonData = XLSX.utils.sheet_to_json(worksheet);

        const isValidRow = (row) => {
          if (this.tab === 0) return row.name && row.code;
          if (this.tab === 1) return row.name;
          if (this.tab === 2) return row.day && row.time;
          return false;
        };

        const validRows = jsonData.filter(isValidRow);
        const invalidRows = jsonData.map((row, i) => {
          const valid = isValidRow(row);
          if (!valid) {
            const reason = this.tab === 0 ? 'Missing name or code' : this.tab === 1 ? 'Missing name' : 'Missing day or time';
            return { row: i + 2, raw: JSON.stringify(row), reason };
          }
          return null;
        }).filter(Boolean);

        if (jsonData.length !== validRows.length) {
          console.warn('Skipped rows due to validation errors:', invalidRows);
          this.snackbarText = `Some invalid rows were skipped: ${invalidRows.length}`;
          this.invalidRows = invalidRows;
          this.invalidDialog = true;
          this.successDialog = true;
          this.revalidateSuccess = validRows.length;
          this.revalidateFailure = invalidRows.length;
          this.snackbar = true;
        }

        if (this.tab === 0) this.courses = validRows;
        else if (this.tab === 1) this.instructors = validRows;
        else this.timeslots = validRows;
      };
      reader.readAsArrayBuffer(file);
    },
    async saveAllChanges() {
      const resources = this.tab === 0 ? this.courses : this.tab === 1 ? this.instructors : this.timeslots;
      for (const item of resources) {
        if (this.unsavedChanges.has(item.id)) {
          if (this.tab === 0) await this.updateCourse(item);
          else if (this.tab === 1) await this.updateInstructor(item);
          else await this.updateTimeslot(item);
        }
      }
    },

    exportData() {
      const resources = this.tab === 0 ? this.courses : this.tab === 1 ? this.instructors : this.timeslots;
      const headers = this.tab === 0 ? ['id', 'name', 'code'] : this.tab === 1 ? ['id', 'name'] : ['id', 'day', 'time'];
      const rows = [headers.join(',')].concat(resources.map(item => headers.map(h => item[h]).join(',')));

      // CSV Export
      const blob = new Blob([rows.join('
')], { type: 'text/csv;charset=utf-8' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${this.tab === 0 ? 'courses' : this.tab === 1 ? 'instructors' : 'timeslots'}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      // XLSX Export
      import('xlsx').then(XLSX => {
        const ws = XLSX.utils.json_to_sheet(resources);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, 'Data');
        XLSX.writeFile(wb, `${this.tab === 0 ? 'courses' : this.tab === 1 ? 'instructors' : 'timeslots'}.xlsx`);
      });
    },
    undoLastChange() {
      if (this.undoStack.length > 0) {
        const last = this.undoStack.pop()
        const resource = this.tab === 0 ? 'course' : this.tab === 1 ? 'instructor' : 'timeslot';
        if (resource === 'course') {
          this.updateCourse(last)
        } else if (resource === 'instructor') {
          this.updateInstructor(last)
        } else {
          this.updateTimeslot(last)
        }
      }
    },
    async addCourse() {
      await createCourse(this.course)
      this.course = { name: '', code: '' }
      this.courses = (await getCourses()).data
    },
    async updateCourse(item) {
      this.undoStack.push({ ...item })
      this.unsavedChanges.add(item.id)
      await updateCourse(item.id, item)
      this.unsavedChanges.delete(item.id)
      this.snackbarText = 'Course updated'
      this.snackbar = true
    },
    async deleteCourse(id) {
      await deleteCourse(id)
      this.courses = (await getCourses()).data
    },

    async addInstructor() {
      await createInstructor(this.instructor)
      this.instructor = { name: '' }
      this.instructors = (await getInstructors()).data
    },
    async updateInstructor(item) {
      this.undoStack.push({ ...item })
      this.unsavedChanges.add(item.id)
      await updateInstructor(item.id, item)
      this.unsavedChanges.delete(item.id)
      this.snackbarText = 'Instructor updated'
      this.snackbar = true
    },
    async deleteInstructor(id) {
      await deleteInstructor(id)
      this.instructors = (await getInstructors()).data
    },

    async addTimeslot() {
      await createTimeslot(this.timeslot)
      this.timeslot = { day: '', time: '' }
      this.timeslots = (await getTimeslots()).data
    },
    async updateTimeslot(item) {
      this.undoStack.push({ ...item })
      this.unsavedChanges.add(item.id)
      await updateTimeslot(item.id, item)
      this.unsavedChanges.delete(item.id)
      this.snackbarText = 'Timeslot updated'
      this.snackbar = true
    },
    async deleteTimeslot(id) {
      await deleteTimeslot(id)
      this.timeslots = (await getTimeslots()).data
    },
  }
}
</script>
