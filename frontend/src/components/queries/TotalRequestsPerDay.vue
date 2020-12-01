<template>
  <div class="container">
    <header class="jumbotron">
      <h3>Total Requests per Day</h3>
      <hr class="my-4"/>
      <p>
        Find the total requests per day for a specific request type and time range.
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
        <label for="type_of_request">Type of Service Request</label>
        <b-form-select
            class="mb-3"
            v-model="typeOfServiceRequest"
            :options="type_of_service_options"
            required
        ></b-form-select>
        <div
            v-if="submitted && errors.has('type_of_request')"
            class="alert-danger"
        >
          {{ errors.first("type_of_request") }}
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
          <td>{{ request.creation_date }}</td>
          <td>{{ request.number_of_requests }}</td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
import QueriesService from "../../services/queries.service";
export default {
  name: "TotalRequestsPerDay",
  data() {
    return {
      startDate: '',
      endDate: '',
      typeOfServiceRequest: '',
      loading: false,
      submitted: false,
      successful: false,
      message: '',
      service_requests: '',
      tableColumns: [
        {
          title: 'Creation Date',
          field: 'creation_date'
        }, {
          title: 'Number of Requests',
          field: 'number_of_requests'
        }
      ],
      type_of_service_options: [
        {value: null, text: "Please select an option"},
        {value: "ABANDONED_VEHICLE", text: "Abandoned Vehicle"},
        {value: "ALLEY_LIGHTS_OUT", text: "Alley Lights Out"},
        {value: "GARBAGE_CART", text: "Garbage Carts"},
        {value: "GRAFFITI", text: "Graffiti Removal"},
        {value: "POT_HOLE", text: "Pot holes Report"},
        {value: "RODENT_BAITING", text: "Rodent Baiting"},
        {value: "SANITATION_CODE", text: "Sanitation Code Complaint"},
        {value: "STREET_LIGHTS_ALL_OUT", text: "Street Lights All Out"},
        {value: "STREET_LIGHT_ONE_OUT", text: "Street Light One Out"},
        {value: "TREE_DEBRIS", text: "Tree Debris"},
        {value: "TREE_TRIM", text: "Tree Trims"},
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
          QueriesService.totalRequestsPerDay(this.startDate, this.endDate, this.typeOfServiceRequest).then(
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