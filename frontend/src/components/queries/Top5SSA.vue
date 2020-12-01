<template>
  <div class="container">
    <header class="jumbotron">
      <h3>Find Top 5 SSA</h3>
      <hr class="my-4"/>
      <p>
        Find the top-5 Special Service Areas (SSA) with regards to total number of requests per day
        for a specific date range (for service requests types that SSA is available: abandoned vehicles,
        garbage carts, graffiti removal, pot holes reported).
      </p>
    </header>
    <form name="form" @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="start_date">Start Date</label>
        <b-input-group class="mb-3">
          <b-form-input
              id="example-input"
              v-model="startDate"
              type="text"
              placeholder="YYYY-MM-DD"
              autocomplete="off"
              required
          ></b-form-input>
          <b-input-group-append>
            <b-form-datepicker
                v-model="startDate"
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
        <label for="end_date">End Date</label>
        <b-input-group class="mb-3">
          <b-form-input
              id="example-input"
              v-model="endDate"
              type="text"
              placeholder="YYYY-MM-DD"
              autocomplete="off"
              required
          ></b-form-input>
          <b-input-group-append>
            <b-form-datepicker
                v-model="endDate"
                button-only
                right
                locale="en-US"
                aria-controls="example-input"
            ></b-form-datepicker>
          </b-input-group-append>
        </b-input-group>
        <div
            v-if="submitted && errors.has('end_date')"
            class="alert-danger"
        >
          {{ errors.first("end_date") }}
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
          <td>{{ request.ssa }}</td>
          <td>{{ request.number_of_requests }}</td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
import QueriesService from "@/services/queries.service";

export default {
  name: "Top5SSA",
  data() {
    return {
      startDate: '',
      endDate: '',
      loading: false,
      submitted: false,
      successful: false,
      message: '',
      tableColumns: [
        {
          title: 'SSA',
          field: 'ssa'
        }, {
          title: 'Number of Requests',
          field: 'number_of_requests'
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
          QueriesService.top5SSA(this.startDate, this.endDate).then(
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