<template>
  <div class="container">
    <header class="jumbotron">
      <h3 v-if="type_of_premises === 'BAITED'">Premises Baited</h3>
      <h3 v-if="type_of_premises === 'GARBAGE'">Premises with Garbage</h3>
      <h3 v-if="type_of_premises === 'RATS'">Premises with Rats</h3>
      <hr class="my-4"/>
      <p v-if="type_of_premises === 'BAITED'">
        Find the rodent baiting requests where the number of premises baited is less than a specified
        number.
      </p>
      <p v-if="type_of_premises === 'GARBAGE'">
        Find the rodent baiting requests where the number of premises with garbage is less than a specified
        number.
      </p>
      <p v-if="type_of_premises === 'RATS'">
        Find the rodent baiting requests where the number of premises with rats is less than a specified
        number.
      </p>
    </header>
    <form name="form" @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="threshold">Threshold</label>
        <b-form-input
            class="mb-3 col-lg mr-1"
            v-model="threshold"
            placeholder="Enter the Threshold"
            type="number"
        >
        </b-form-input>
        <div v-if="submitted && errors.has('threshold')" class="alert-danger">
          {{ errors.first("threshold") }}
        </div>
        <label for="page">Page</label>
        <b-form-input
            class="mb-3 col-lg ml-1"
            v-model="page"
            placeholder="Enter the Page"
            type="number"
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
  name: "RodentBaiting",
  data() {
    return {
      type_of_premises: '',
      threshold: '',
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
  beforeRouteUpdate(to) {
    this.name = to.params.name
  },
  created() {
    this.$forceUpdate()
    const route = this.$router.currentRoute;
    console.log(route.path)
    if (route.path === '/premises-baited') {
      this.type_of_premises = 'BAITED';
    } else if (route.path === '/premises-garbage') {
      this.type_of_premises = 'GARBAGE';
    } else if (route.path === '/premises-rats') {
      this.type_of_premises = 'RATS';
    }
  },
  methods: {
    handleSubmit() {
      this.message = '';
      this.submitted = true;
      this.loading = true;
      this.$validator.validate().then((isValid) => {
        if (isValid) {
          QueriesService.rodentBaiting(this.page, this.threshold, this.type_of_premises).then(
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