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
          <router-link to="" class="nav-link">
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
      <router-view />
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
