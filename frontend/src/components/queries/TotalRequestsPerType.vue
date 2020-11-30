<template>
  <div class="container">
    <header class="jumbotron">
      <h3>Total Requests per Type</h3>
      <hr class="my-4"/>
      <p>
        Find the total requests per type that were created within a specified time range and sort them in a
        descending order.
      </p>
    </header>
    <form name="form" @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="startDate">Start Date</label>
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
            v-if="submitted && errors.has('startDate')"
            class="alert-danger"
        >
          {{ errors.first("start_date") }}
        </div>
        <label for="endDate">End Date</label>
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
            v-if="submitted && errors.has('endDate')"
            class="alert-danger"
        >
          {{ errors.first("endDate") }}
        </div>
        <div class="form-group">
          <button class="btn btn-primary">Submit</button>
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
            <td>{{ request.type_of_service_request }}</td>
            <td>{{ request.number_of_requests }}</td>
          </tr>
      </table>
    </div>
  </div>
</template>

<script>
import QueriesService from "../../services/queries.service";

export default {
  name: "TotalRequestsPerType",
  data() {
    return {
      startDate: '',
      endDate: '',
      submitted: false,
      successful: false,
      message: '',
      service_requests: '',
      tableColumns: [
        {
          title: 'Type of Service Request',
          field: 'type_of_service_request'
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
      this.$validator.validate().then((isValid) => {
        if (isValid) {
          QueriesService.totalRequestsPerType(this.startDate, this.endDate).then(
              (response) => {
                this.successful = true;
                this.message = response.data;
                // this.message = response.status;
              },
              (error) => {
                console.log(error.message)
                this.message = error.response.data;
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