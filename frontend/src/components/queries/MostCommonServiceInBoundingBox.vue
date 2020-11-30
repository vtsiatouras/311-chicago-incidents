<template>
  <div class="container">
    <header class="jumbotron">
      <h3>Most Common Service in Bounding Box</h3>
      <hr class="my-4"/>
      <p>
        Find the most common service request in a specified bounding box (as designated by GPS-
        coordinates) for a specific day.
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
        <label for="latitude">Point A</label>
        <form class="form-inline">
          <b-form-input
              class="mb-3 col-lg mr-1"
              v-model="a_latitude"
              placeholder="Enter the Latitude"
              type="number"
              step="0.000000000001"
          >
          </b-form-input>
          <div v-if="submitted && errors.has('latitude')" class="alert-danger">
            {{ errors.first("latitude") }}
          </div>
          <b-form-input
              class="mb-3 col-lg ml-1"
              v-model="a_longitude"
              placeholder="Enter the Longitude"
              type="number"
              step="0.000000000001"
          >
          </b-form-input>
          <div v-if="submitted && errors.has('longitude')" class="alert-danger">
            {{ errors.first("longitude") }}
          </div>
        </form>
        <label for="latitude">Point B</label>
        <form class="form-inline">
          <b-form-input
              class="mb-3 col-lg mr-1"
              v-model="b_latitude"
              placeholder="Enter the Latitude"
              type="number"
              step="0.000000000001"
          >
          </b-form-input>
          <div v-if="submitted && errors.has('latitude')" class="alert-danger">
            {{ errors.first("latitude") }}
          </div>
          <b-form-input
              class="mb-3 col-lg ml-1"
              v-model="b_longitude"
              placeholder="Enter the Longitude"
              type="number"
              step="0.000000000001"
          >
          </b-form-input>
          <div v-if="submitted && errors.has('longitude')" class="alert-danger">
            {{ errors.first("longitude") }}
          </div>
        </form>
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
          <td>{{ request.type_of_service_request }}</td>
          <td>{{ request.number_of_requests }}</td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
import QueriesService from "@/services/queries.service";

export default {
  name: "MostCommonServiceInBoundingBox",
  data() {
    return {
      date: '',
      a_latitude: '',
      a_longitude: '',
      b_latitude: '',
      b_longitude: '',
      loading: false,
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
      this.loading = true;
      this.$validator.validate().then((isValid) => {
        if (isValid) {
          QueriesService.mostCommonServiceInBoundingBox(this.date, this.a_latitude, this.a_longitude,
              this.b_latitude, this.b_longitude).then(
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