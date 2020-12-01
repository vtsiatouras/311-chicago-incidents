<template>
  <div class="container">
    <header class="jumbotron">
      <h3>Police Districts</h3>
      <hr class="my-4"/>
      <p>
        Find the police districts that have handled “pot holes” requests with more than one number
        of potholes on the same day that they also handled “rodent baiting” requests with more than
        one number of premises baited, for a specific day.
      </p>
    </header>
    <form name="form" @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="start_date">Date</label>
        <b-input-group class="mb-3">
          <b-form-input
              id="example-input"
              v-model="date"
              type="text"
              placeholder="YYYY-MM-DD"
              autocomplete="off"
              required
          ></b-form-input>
          <b-input-group-append>
            <b-form-datepicker
                v-model="date"
                button-only
                right
                locale="en-US"
                aria-controls="example-input"
            ></b-form-datepicker>
          </b-input-group-append>
        </b-input-group>
        <div
            v-if="submitted && errors.has('start_date')"
            class="alert-danger"
        >
          {{ errors.first("start_date") }}
        </div>
        <div class="form-group">
          <button class="btn btn-primary center-block" :disabled="loading">
            <span
                v-show="loading"
                class="spinner-border spinner-border-sm"
            ></span>
            <span>Submit</span>
          </button>
        </div>
      </div>
      <div class="form-group">
        <div v-if="message && !successful" class="alert alert-danger" role="alert">
          {{ message }}
        </div>
      </div>
    </form>
    <div v-if="message && successful">
      <table v-if="message" class="table">
        <thead>
        <tr>
          <th v-for="column in tableColumns" v-bind:key="column.id">
            {{ column.title }}
          </th>
        </tr>
        </thead>
        <tr v-for="request in message" v-bind:key="request.id">
          <td>{{ request.police_district }}</td>
          <td>{{ request.rodent_baiting_sum }}</td>
          <td>{{ request.potholes_sum }}</td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
import QueriesService from "@/services/queries.service";

export default {
  name: "PoliceDistricts",
  data() {
    return {
      date: '',
      loading: false,
      submitted: false,
      successful: false,
      message: '',
      tableColumns: [
        {
          title: 'Police District',
          field: 'police_district'
        }, {
          title: 'Rodent Baiting Sum',
          field: 'rodent_baiting_sum'
        }, {
          title: 'Potholes Sum',
          field: 'potholes_sum'
        }
      ],
    };
  },
  methods: {
    handleSubmit() {
      this.message = '';
      this.submitted = true;
      this.loading = true;
      this.$validator.validate().then((isValid) => {
        if (isValid) {
          QueriesService.policeDistricts(this.date).then(
              (response) => {
                this.successful = true;
                this.message = response.data;
                this.loading = false;
              },
              (error) => {
                console.log(error.message)
                this.message = error.response.data;
                this.loading = false;
              }
          );
        }
      });
    }
  }
};
</script>

<style scoped>

</style>