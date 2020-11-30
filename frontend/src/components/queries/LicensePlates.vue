<template>
  <div class="container">
    <header class="jumbotron">
      <h3>License Plates</h3>
      <hr class="my-4"/>
      <p>
        Find the license plates (if any) that have been involved in abandoned vehicle complaints more
        than once.
      </p>
    </header>
    <form name="form" @submit.prevent="handleSubmit">
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
          <td>{{ request.license_plate }}</td>
          <td>{{ request.number_of_requests }}</td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
import QueriesService from "@/services/queries.service";

export default {
  name: "LicensePlates",
  data() {
    return {
      loading: false,
      submitted: false,
      successful: false,
      message: '',
      tableColumns: [
        {
          title: 'License Plate',
          field: 'license_plate'
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
          QueriesService.licensePlates().then(
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