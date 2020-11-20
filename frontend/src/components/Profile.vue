<!--This page will include queries etc.-->
<template>
  <div class="container">
    <header class="jumbotron">
      <h3>
        <strong>{{ userName }}</strong> Profile
      </h3>
    </header>
    <div>
      <strong>User Info</strong>
      <p></p>
      <p>User ID: {{ userId }}</p>
      <p>Username: {{ userName }}</p>
      <p>User Email: {{ userEmail }}</p>
    </div>
  </div>
</template>

<script>
import UserService from "../services/user.service";

export default {
  name: "Profile",
  data() {
    return {
      userId: null,
      userName: null,
      userEmail: null,
    };
  },
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    },
  },
  mounted() {
    if (!this.currentUser) {
      this.$router.push("/login");
    }
    [
      this.userId,
      this.userName,
      this.userEmail,
    ] = UserService.getUserInfoFromToken();
  },
};
</script>
