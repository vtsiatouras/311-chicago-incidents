<template>
  <div class="container">
    <header class="jumbotron">
      <h3>Search Incidents</h3>
      <hr class="my-4"/>
      <p>
        Find the incidents that happened at the specified address or zipcode.
      </p>
    </header>
    <form name="form" @submit.prevent="handleSubmit">
      <label for="street_address">Street Address</label>
      <b-form-input
          class="mb-3"
          v-model="streetAddress"
          placeholder="Enter the Street Address"
      >
      </b-form-input>
      <div
          v-if="submitted && errors.has('street_address')"
          class="alert-danger"
      >
        {{ errors.first("street_address") }}
      </div>
      <label for="zip_code">Zip Code</label>
      <b-form-input
          class="mb-3"
          v-model="zipcode"
          placeholder="Enter the Zip Code"
      >
      </b-form-input>
      <div v-if="submitted && errors.has('zip_code')" class="alert-danger">
        {{ errors.first("zip_code") }}
      </div>
      <label for="page">Page</label>
      <b-form-input
          class="mb-3 col-lg ml-1"
          v-model="page"
          placeholder="Enter the Page"
          type="number"
          required
      >
      </b-form-input>
      <div v-if="submitted && errors.has('page')" class="alert-danger">
        {{ errors.first("page") }}
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
          <td>{{ request.id }}</td>
          <td>{{ request.service_request_number }}</td>
          <td>{{ request.type_of_service_request }}</td>
          <td>{{ request.street_address }}</td>
          <td>{{ request.zip_code }}</td>
          <td>{{ request.latitude }}</td>
          <td>{{ request.longitude }}</td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
import QueriesService from "@/services/queries.service";

export default {
  name: "SearchIncidents",
  data() {
    return {
      streetAddress: '',
      zipcode: '',
      page: '',
      loading: false,
      submitted: false,
      successful: false,
      message: '',
      tableColumns: [
        {
          title: 'ID',
          field: 'id'
        }, {
          title: 'Service Request Number',
          field: 'service_request_number'
        }, {
          title: 'Type of Service Request',
          field: 'type_of_service_request'
        }, {
          title: 'Street Address',
          field: 'street_address'
        }, {
          title: 'Zipcode',
          field: 'zip_code'
        }, {
          title: 'Latitude',
          field: 'latitude'
        }, {
          title: 'Longitude',
          field: 'longitude'
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
          QueriesService.searchIncidents(this.page, this.streetAddress, this.zipcode).then(
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