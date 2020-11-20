<template>
  <div class="container">
    <header class="jumbotron">
      <h3>Create an Incident</h3>
      <hr class="my-4" />
      <p>
        Here you can create any type of incident you want. Just fill the fields
        below.
      </p>
    </header>
    <form name="form" @submit.prevent="handleSubmit">
      <div v-if="!successful">
        <h4>Incident Basic Information</h4>
        <div class="form-group">
          <label for="creation_date">Creation Date</label>
          <b-input-group class="mb-3">
            <b-form-input
              id="example-input"
              v-model="incident.creation_date"
              type="text"
              placeholder="YYYY-MM-DD"
              autocomplete="off"
              required
            ></b-form-input>
            <b-input-group-append>
              <b-form-datepicker
                v-model="incident.creation_date"
                button-only
                right
                locale="en-US"
                aria-controls="example-input"
              ></b-form-datepicker>
            </b-input-group-append>
          </b-input-group>
          <div
            v-if="submitted && errors.has('creation_date')"
            class="alert-danger"
          >
            {{ errors.first("creation_date") }}
          </div>
          <label for="completion_date">Completion Date</label>
          <b-input-group class="mb-3">
            <b-form-input
              id="example-input"
              v-model="incident.completion_date"
              type="text"
              placeholder="YYYY-MM-DD"
              autocomplete="off"
            ></b-form-input>
            <b-input-group-append>
              <b-form-datepicker
                v-model="incident.completion_date"
                button-only
                right
                locale="en-US"
                aria-controls="example-input"
              ></b-form-datepicker>
            </b-input-group-append>
          </b-input-group>
          <div
            v-if="submitted && errors.has('completion_date')"
            class="alert-danger"
          >
            {{ errors.first("completion_date") }}
          </div>
          <label for="status">Status</label>
          <b-form-select
            class="mb-3"
            v-model="incident.status"
            :options="status_options"
            placeholder="Enter Most Recent Action (if any)"
            required
          ></b-form-select>
          <div v-if="submitted && errors.has('status')" class="alert-danger">
            {{ errors.first("status") }}
          </div>
          <label for="service_request_number">Service Request Number</label>
          <b-form-input
            class="mb-3"
            v-model="incident.service_request_number"
            placeholder="Enter Service Request Number"
            required
          >
          </b-form-input>
          <div
            v-if="submitted && errors.has('service_request_number')"
            class="alert-danger"
          >
            {{ errors.first("service_request_number") }}
          </div>
          <label for="type_of_request">Type of Service Request</label>
          <b-form-select
            class="mb-3"
            v-model="incident.type_of_service_request"
            :options="type_of_service_options"
            required
          ></b-form-select>
          <div
            v-if="submitted && errors.has('type_of_request')"
            class="alert-danger"
          >
            {{ errors.first("type_of_request") }}
          </div>
          <label for="service_request_number">Street Address</label>
          <b-form-input
            class="mb-3"
            v-model="incident.street_address"
            placeholder="Enter the Street Address"
            required
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
            v-model="incident.zip_code"
            placeholder="Enter the Zip Code"
          >
          </b-form-input>
          <div v-if="submitted && errors.has('zip_code')" class="alert-danger">
            {{ errors.first("zip_code") }}
          </div>
          <label for="x_coordinate">X Coordinate</label>
          <b-form-input
            class="mb-3"
            v-model="incident.x_coordinate"
            placeholder="Enter the X Coordinate"
            type="number"
            step="0.000000000001"
          >
          </b-form-input>
          <div
            v-if="submitted && errors.has('x_coordinate')"
            class="alert-danger"
          >
            {{ errors.first("x_coordinate") }}
          </div>
          <label for="y_coordinate">Y Coordinate</label>
          <b-form-input
            class="mb-3"
            v-model="incident.y_coordinate"
            placeholder="Enter the Y Coordinate"
            type="number"
            step="0.000000000001"
          >
          </b-form-input>
          <div
            v-if="submitted && errors.has('y_coordinate')"
            class="alert-danger"
          >
            {{ errors.first("y_coordinate") }}
          </div>
          <label for="latitude">Latitude</label>
          <b-form-input
            class="mb-3"
            v-model="incident.latitude"
            placeholder="Enter the Latitude"
            type="number"
            step="0.000000000001"
          >
          </b-form-input>
          <div v-if="submitted && errors.has('latitude')" class="alert-danger">
            {{ errors.first("latitude") }}
          </div>
          <label for="longitude">Longitude</label>
          <b-form-input
            class="mb-3"
            v-model="incident.longitude"
            placeholder="Enter the Longitude"
            type="number"
            step="0.000000000001"
          >
          </b-form-input>
          <div v-if="submitted && errors.has('longitude')" class="alert-danger">
            {{ errors.first("longitude") }}
          </div>
          <label for="ward">Ward</label>
          <b-form-input
            class="mb-3"
            v-model="incident.ward"
            placeholder="Enter the ward"
            type="number"
          >
          </b-form-input>
          <div v-if="submitted && errors.has('ward')" class="alert-danger">
            {{ errors.first("ward") }}
          </div>
          <label for="police_district">Police District</label>
          <b-form-input
            class="mb-3"
            v-model="incident.police_district"
            placeholder="Enter the Police District"
            type="number"
          >
          </b-form-input>
          <div
            v-if="submitted && errors.has('police_district')"
            class="alert-danger"
          >
            {{ errors.first("police_district") }}
          </div>
          <label for="community_area">Community Area</label>
          <b-form-input
            class="mb-3"
            v-model="incident.community_area"
            placeholder="Enter the Community Area"
            type="number"
          >
          </b-form-input>
          <div
            v-if="submitted && errors.has('community_area')"
            class="alert-danger"
          >
            {{ errors.first("community_area") }}
          </div>
          <label for="ssa">SSA</label>
          <b-form-input
            class="mb-3"
            v-model="incident.ssa"
            placeholder="Enter the SSA"
            type="number"
          >
          </b-form-input>
          <div v-if="submitted && errors.has('ssa')" class="alert-danger">
            {{ errors.first("ssa") }}
          </div>
          <label for="census_tracts">Census Tracts</label>
          <b-form-input
            class="mb-3"
            v-model="incident.census_tracts"
            placeholder="Enter the Census Tracts"
            type="number"
          >
          </b-form-input>
          <div
            v-if="submitted && errors.has('census_tracts')"
            class="alert-danger"
          >
            {{ errors.first("census_tracts") }}
          </div>
          <label for="zip_codes">Zip Codes (Appears in newer datasets)</label>
          <b-form-input
            class="mb-3"
            v-model="incident.zip_codes"
            placeholder="Enter the Zip Codes"
            type="number"
          >
          </b-form-input>
          <div v-if="submitted && errors.has('zip_codes')" class="alert-danger">
            {{ errors.first("zip_codes") }}
          </div>
          <label for="wards">Wards (Appears in newer datasets)</label>
          <b-form-input
            class="mb-3"
            v-model="incident.wards"
            placeholder="Enter the Wards"
            type="number"
          >
          </b-form-input>
          <div v-if="submitted && errors.has('wards')" class="alert-danger">
            {{ errors.first("wards") }}
          </div>
          <label for="historical_wards_03_15">Historical Wards 2003-2015</label>
          <b-form-input
            class="mb-3"
            v-model="incident.historical_wards_03_15"
            placeholder="Enter the Wards"
            type="number"
          >
          </b-form-input>
          <div
            v-if="submitted && errors.has('historical_wards_03_15')"
            class="alert-danger"
          >
            {{ errors.first("historical_wards_03_15") }}
          </div>
          <label for="community_areas"
            >Community Areas (Appears in newer datasets)</label
          >
          <b-form-input
            class="mb-3"
            v-model="incident.community_areas"
            placeholder="Enter the Community Areas"
            type="number"
          >
          </b-form-input>
          <div
            v-if="submitted && errors.has('community_areas')"
            class="alert-danger"
          >
            {{ errors.first("community_areas") }}
          </div>
        </div>
        <div
          class="form-group"
          v-if="
            [
              'ABANDONED_VEHICLE',
              'GARBAGE_CART',
              'POT_HOLE',
              'RODENT_BAITING',
              'TREE_DEBRIS',
            ].includes(incident.type_of_service_request)
          "
        >
          <h4>Incident Activity</h4>
          <label for="current_activity">Current Activity</label>
          <b-form-input
            class="mb-3"
            v-model="incidentActivity.current_activity"
            placeholder="Enter Current Activity (if any)"
          >
          </b-form-input>
          <div
            v-if="submitted && errors.has('current_activity')"
            class="alert-danger"
          >
            {{ errors.first("current_activity") }}
          </div>
          <label for="most_recent_action">Most Recent Action</label>
          <b-form-input
            class="mb-3"
            v-model="incidentActivity.most_recent_action"
            placeholder="Enter Most Recent Action (if any)"
          >
          </b-form-input>
          <div
            v-if="submitted && errors.has('most_recent_action')"
            class="alert-danger"
          >
            {{ errors.first("most_recent_action") }}
          </div>
        </div>
        <div
          class="form-group"
          v-if="incident.type_of_service_request === 'ABANDONED_VEHICLE'"
        >
          <h4>Abandoned Vehicle Details</h4>
          <label for="license_plate">License Plate</label>
          <b-form-input
            class="mb-3"
            v-model="abandonedVehicle.license_plate"
            placeholder="Enter License Plate"
          >
          </b-form-input>
          <div
            v-if="submitted && errors.has('license_plate')"
            class="alert-danger"
          >
            {{ errors.first("license_plate") }}
          </div>
          <label for="vehicle_make_model">Vehicle Make/Model</label>
          <b-form-input
            class="mb-3"
            v-model="abandonedVehicle.vehicle_make_model"
            placeholder="Enter Vehicle's Make or Model"
          >
          </b-form-input>
          <div
            v-if="submitted && errors.has('vehicle_make_model')"
            class="alert-danger"
          >
            {{ errors.first("vehicle_make_model") }}
          </div>
          <label for="vehicle_color">Vehicle Color</label>
          <b-form-input
            class="mb-3"
            v-model="abandonedVehicle.vehicle_color"
            placeholder="Enter Vehicle's Color"
          >
          </b-form-input>
          <div
            v-if="submitted && errors.has('vehicle_color')"
            class="alert-danger"
          >
            {{ errors.first("vehicle_color") }}
          </div>
        </div>
        <div
          class="form-group"
          v-if="
            ['GARBAGE_CART', 'POT_HOLE'].includes(
              incident.type_of_service_request
            )
          "
        >
          <div v-if="incident.type_of_service_request === 'GARBAGE_CART'">
            <h4>Garbage Cart Details</h4>
            <label for="number_of_elements">Number of Carts</label>
          </div>
          <div v-if="incident.type_of_service_request === 'POT_HOLE'">
            <h4>Potholes Details</h4>
            <label for="number_of_elements">Number of Potholes</label>
          </div>
          <b-form-input
            class="mb-3"
            v-model="garbageCartPorthole.number_of_elements"
            type="number"
            placeholder="Enter the Number of Elements"
          >
          </b-form-input>
          <div
            v-if="submitted && errors.has('license_plate')"
            class="alert-danger"
          >
            {{ errors.first("license_plate") }}
          </div>
        </div>
        <div
          class="form-group"
          v-if="incident.type_of_service_request === 'GRAFFITI'"
        >
          <h4>Graffiti Removal Details</h4>
          <label for="surface">Surface</label>
          <b-form-input
            class="mb-3"
            v-model="graffiti.surface"
            placeholder="Enter the Surface"
          >
          </b-form-input>
          <div v-if="submitted && errors.has('surface')" class="alert-danger">
            {{ errors.first("surface") }}
          </div>
          <label for="location">Location</label>
          <b-form-input
            class="mb-3"
            v-model="graffiti.location"
            placeholder="Enter the location"
          >
          </b-form-input>
          <div v-if="submitted && errors.has('location')" class="alert-danger">
            {{ errors.first("location") }}
          </div>
        </div>
        <div
          class="form-group"
          v-if="incident.type_of_service_request === 'SANITATION_CODE'"
        >
          <h4>Sanitation Code Violation Complaint</h4>
          <label for="nature_of_code_violation">Nature of Code Violation</label>
          <b-form-input
            class="mb-3"
            v-model="sanitationCode.nature_of_code_violation"
            placeholder="Enter the Code Violation"
          >
          </b-form-input>
          <div
            v-if="submitted && errors.has('nature_of_code_violation')"
            class="alert-danger"
          >
            {{ errors.first("nature_of_code_violation") }}
          </div>
        </div>
        <div
          class="form-group"
          v-if="
            ['TREE_TRIM', 'TREE_DEBRIS'].includes(
              incident.type_of_service_request
            )
          "
        >
          <div v-if="incident.type_of_service_request === 'TREE_TRIM'">
            <h4>Tree Trims Details</h4>
          </div>
          <div v-if="incident.type_of_service_request === 'TREE_DEBRIS'">
            <h4>Tree Debris Details</h4>
          </div>
          <label for="location">Location</label>
          <b-form-input
            class="mb-3"
            v-model="tree.location"
            placeholder="Enter the Location"
          >
          </b-form-input>
          <div v-if="submitted && errors.has('location')" class="alert-danger">
            {{ errors.first("location") }}
          </div>
        </div>
        <div class="form-group">
          <button class="btn btn-primary">Submit</button>
        </div>
        <div class="form-group">
          <div v-if="message" class="alert alert-danger" role="alert">
            {{ message }}
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import Incident from "@/models/incident";
import IncidentActivity from "@/models/incidentActivity";
import AbandonedVehicle from "@/models/abandonedVehicle";
import GarbageCartsPotholes from "@/models/garbageCartsPotholes";
import Graffiti from "@/models/graffiti";
import RodentBaiting from "@/models/rodentBaiting";
import SanitationCode from "@/models/sanitationCode";
import Tree from "@/models/tree";
import CreateIncidentService from "../services/create-incident.service";

export default {
  name: "IncidentCreate",
  data() {
    return {
      incident: new Incident(
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        ""
      ),
      incidentActivity: new IncidentActivity("", ""),
      abandonedVehicle: new AbandonedVehicle("", "", ""),
      garbageCartPorthole: new GarbageCartsPotholes(""),
      graffiti: new Graffiti("", ""),
      rodentBaiting: new RodentBaiting("", "", ""),
      sanitationCode: new SanitationCode(""),
      tree: new Tree(""),
      status_options: [
        { value: null, text: "Please select an option" },
        { value: "OPEN", text: "Open" },
        { value: "OPEN_DUP", text: "Open - Duplicate" },
        { value: "COMPLETED", text: "Completed" },
        { value: "COMPLETED_DUP", text: "Completed - Duplicate" },
      ],
      type_of_service_options: [
        { value: null, text: "Please select an option" },
        { value: "ABANDONED_VEHICLE", text: "Abandoned Vehicle" },
        { value: "ALLEY_LIGHTS_OUT", text: "Alley Lights Out" },
        { value: "GARBAGE_CART", text: "Garbage Carts" },
        { value: "GRAFFITI", text: "Graffiti Removal" },
        { value: "POT_HOLE", text: "Pot holes Report" },
        { value: "RODENT_BAITING", text: "Rodent Baiting" },
        { value: "SANITATION_CODE", text: "Sanitation Code Complaint" },
        { value: "STREET_LIGHTS_ALL_OUT", text: "Street Lights All Out" },
        { value: "STREET_LIGHT_ONE_OUT", text: "Street Light One Out" },
        { value: "TREE_DEBRIS", text: "Tree Debris" },
        { value: "TREE_TRIM", text: "Tree Trims" },
      ],
      submitted: false,
      successful: false,
      message: "",
    };
  },
  methods: {
    handleSubmit() {
      this.message = "";
      this.submitted = true;
      this.$validator.validate().then((isValid) => {
        if (isValid) {
          this.serviceDispatcher().then(
              () => {
                this.successful = true;
                this.$router.push("/home");
              },
              (error) => {
                console.log(error.message)
                this.message = error.response.data;
              }
          );
        }
      });
    },
    serviceDispatcher() {
      if (this.incident.type_of_service_request === "ABANDONED_VEHICLE") {
        return CreateIncidentService.abandonedVehicleIncident(this.incident, this.incidentActivity,
            this.abandonedVehicle)
        // } else if (['GARBAGE_CART', 'POT_HOLE'].includes(this.incident.type_of_service_request)) {
        //
        // } else if (this.incident.type_of_service_request === 'GRAFFITI') {
        //
        // } else if (this.incident.type_of_service_request === 'RODENT_BAITING') {
        //
        // } else if (this.incident.type_of_service_request === 'SANITATION_CODE') {
        //
        // } else if (['TREE_TRIM', 'TREE_DEBRIS'].includes(this.incident.type_of_service_request)) {
      } else {
        return CreateIncidentService.incident(this.incident)
      }
    },
  },
};
</script>
<style scoped>
</style>
