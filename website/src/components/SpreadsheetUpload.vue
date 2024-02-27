<template>
  <v-container class="size" fluid grid-list-xl>
    <v-stepper v-model="element">

      <v-stepper-header>
        <v-stepper-step :complete="element > 1" step="1">Spreadsheet Type</v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step :complete="element > 2" step="2">Upload Spreadsheet</v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step :complete="element > 3" step="3">Review</v-stepper-step>
      </v-stepper-header>

      <v-stepper-items>
        <v-stepper-content step="1" >
          <h1>Spreadsheet Type</h1>
        </v-stepper-content>

        <v-stepper-content step="2" >
          <h1>Upload Spreadsheet</h1>
        </v-stepper-content>

        <v-stepper-content step="3" >
          <h1>Review</h1>
        </v-stepper-content>

      </v-stepper-items>

      <v-footer style="left: 50%; margin-right: -50%; transform: translate(-50%, 0); max-width: 600px"
                fixed height="auto">
        <v-btn v-if="element !== 3" color="primary" flat large @click=back>
          <v-icon>arrow_back</v-icon>
          Back
        </v-btn>
        <v-spacer></v-spacer>

        <v-btn color="primary" v-if="element !== 3" flat large @click=next right>
          Next
          <v-icon>arrow_forward</v-icon>
        </v-btn>

        <v-btn color="primary" v-if="element === 3" flat large right
          v-bind:loading="this.isLoading"
          @click="onUploadSpreadsheet(password)">
           Set Order Items
        </v-btn>
      </v-footer>
    </v-stepper>
  </v-container>
</template>

<script>
import store from '../store';

export default {
  name: "SpreadsheetUpload",
  store,
  computed: {
    password() {
      return this.$store.getters.getPassword;
    },
  },
  methods: {
    onUploadSpreadsheet(password) {
      console.log('Password: ', password);
      this.isLoading = true;
    },
    next() {
      this.element++;
    },
    back() {
      this.element--;
    },
  },
  data: () => ({
    element: 1,
    isLoading: false,
  })
}
</script>

<style scoped>
.size {
  max-width: 100%;
  width: 600px;
}
</style>
