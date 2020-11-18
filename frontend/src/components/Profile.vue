<!--This page will include queries etc.-->
<template>
  <div class="container">
    <header class="jumbotron">
      <h3>
        <strong>{{ currentUser.username }}</strong> Profile
      </h3>
    </header>
    <p>
      <strong>Token:</strong>
      {{ currentUser.access }}
    </p>
    <p>
      <strong>User Info</strong>
      <strong> ID: {{ id }} </strong>
      Username: {{ username }}
      Email: {{ email }}
    </p>
  </div>
</template>

<script>
import UserService from '../services/user.service';

export default {
  name: 'Profile',
  data() {
    return {
      id: null,
      username: null,
      email: null
    }
  },
  methods: {
    getUserInformation() {
      UserService.getUserInfo().then(
          response => {
            let resp = response.data;
            this.id = resp[0].id
            this.username = resp[0].username
            this.email = resp[0].email
          },
          error => {
            this.content =
                (error.response && error.response.data) ||
                error.message ||
                error.toString();
          }
      );
    }
  },
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    }
  },
  mounted() {
    if (!this.currentUser) {
      this.$router.push('/login');
    }
    this.getUserInformation()
  }
};
</script>
