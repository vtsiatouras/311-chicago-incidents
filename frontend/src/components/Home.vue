<template>
  <div class="container">
    <header class="jumbotron">
      <h3>Chicago Incidents Actions</h3>
    </header>
    <button class="btn btn-primary" @click="$router.push('create-incident')">
      Create an Incident
    </button>
  </div>
</template>

<script>
export default {
  name: "Home",
  data() {
    return {
      content: "",
    };
  },
  mounted() {},
};
</script>
