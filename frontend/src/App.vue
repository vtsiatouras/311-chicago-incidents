<template>
  <div id="app">
    <nav class="navbar navbar-expand navbar-dark bg-dark">
      <a href class="navbar-brand" @click.prevent>311 Chicago Incidents</a>
      <div v-if="currentUser" class="navbar-nav mr-auto">
        <li class="nav-item">
          <router-link to="/home" class="nav-link">
            <font-awesome-icon icon="home" />
            Home
          </router-link>
        </li>
      </div>

      <div v-if="currentUser" class="navbar-nav mr-auto">
        <li class="nav-item">
          <router-link to="/create-incident" class="nav-link">
            <font-awesome-icon icon="plus-square" />
            Create an Incident
          </router-link>
        </li>
      </div>

      <div v-if="currentUser" class="navbar-nav mr-auto">
        <li class="nav-item">
          <router-link to="/search-incidents" class="nav-link">
            <font-awesome-icon icon="search" />
            Search Incidents
          </router-link>
        </li>
      </div>

      <div v-if="currentUser" class="navbar-nav mr-auto">
        <li class="nav-item" >
          <b-nav-item-dropdown variant="dark">
            <template slot="button-content">
              <font-awesome-icon icon="database" />
              Queries
            </template>
            <b-dropdown-item>
              <router-link to="/total-requests-per-type" class="dropdown-item">
                1. Total requests per type
              </router-link>
            </b-dropdown-item>
            <b-dropdown-item>
              <router-link to="/total-requests-per-day" class="dropdown-item">
                2. Total requests per day
              </router-link>
            </b-dropdown-item>
            <b-dropdown-item>
              <router-link to="/most-common-service-per-zipcode" class="dropdown-item">
                3. Most common service per zipcode
              </router-link>
            </b-dropdown-item>
            <b-dropdown-item>
              <router-link to="/average-completion-time-per-request" class="dropdown-item">
                4. Average completion time per request
              </router-link>
            </b-dropdown-item>
            <b-dropdown-item>
              <router-link to="/most-common-service-in-bounding-box" class="dropdown-item">
                5. Most common service in bounding box
              </router-link>
            </b-dropdown-item>
            <b-dropdown-item>
              <router-link to="/top-5-ssa" class="dropdown-item">
                6. Top 5 SSA
              </router-link>
            </b-dropdown-item>
            <b-dropdown-item>
              <router-link to="/license-plates" class="dropdown-item">
                7. License plates
              </router-link>
            </b-dropdown-item>
            <b-dropdown-item>
              <router-link to="/second-most-common-color" class="dropdown-item">
                8. Second most common vehicle color
              </router-link>
            </b-dropdown-item>
            <b-dropdown-item>
              <router-link to="/premises-baited" class="dropdown-item">
                9. Rodent baiting - baited premises
              </router-link>
            </b-dropdown-item>
            <b-dropdown-item>
              <router-link to="/premises-garbage" class="dropdown-item">
                10. Rodent baiting - premises with garbage
              </router-link>
            </b-dropdown-item>
            <b-dropdown-item>
              <router-link to="/premises-rats" class="dropdown-item">
                11. Rodent baiting - premises with rats
              </router-link>
            </b-dropdown-item>
            <b-dropdown-item>
              <router-link to="/police-districts" class="dropdown-item">
                12. Police districts
              </router-link>
            </b-dropdown-item>
          </b-nav-item-dropdown>
        </li>
      </div>

      <div v-if="!currentUser" class="navbar-nav ml-auto">
        <li class="nav-item">
          <router-link to="/register" class="nav-link">
            <font-awesome-icon icon="user-plus" />
            Sign Up
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/login" class="nav-link">
            <font-awesome-icon icon="sign-in-alt" />
            Login
          </router-link>
        </li>
      </div>

      <div v-if="currentUser" class="navbar-nav ml-auto">
        <li class="nav-item">
          <router-link to="/profile" class="nav-link">
            <font-awesome-icon icon="user" />
            {{ userName }}
          </router-link>
        </li>
        <li class="nav-item">
          <a class="nav-link" href @click.prevent="logOut">
            <font-awesome-icon icon="sign-out-alt" />
            LogOut
          </a>
        </li>
      </div>
    </nav>

    <div class="container">
      <router-view :key="$route.fullPath"></router-view>
    </div>
  </div>
</template>

<script>
import UserService from "@/services/user.service";

export default {
  data() {
    return {
      userId: null,
      userName: null,
      userEmail: null,
    };
  },
  created () {
    document.title = "311 Chicago Incidents";
  },
  computed: {
    currentUser() {
      [
        this.userId,
        this.userName,
        this.userEmail,
      ] = UserService.getUserInfoFromToken();
      return this.$store.state.auth.user;
    },
  },
  methods: {
    logOut() {
      this.$store.dispatch("auth/logout");
      this.$router.push("/login");
    },
  },
};
</script>
