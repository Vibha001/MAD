<template>
  <div class="container-fluid">
    <nav
      class="navbar navbar-expand-lg navbar-light bg-light fixed-top"
      style="font-size: 24px; padding: 20px"
    >
      <h4>{{ username }}'s Dashboard</h4>
      |
      <br />
      <router-link to="/admin_dashboard"> Dashboard </router-link> |<br />
      <router-link to="/summary"> Summary </router-link> |<br />
      <LogOutButton />
    </nav>
    <Theatre />
    <br /><br /><br /><br />
  </div>
</template>

<script>
import LogOutButton from "../views/Logout.vue"; // Import the LogOut component
import Theatre from "../components/Theatre.vue";

import { onMounted, ref } from "vue";
export default {
  name: "AdminDash",
  data: function () {
    return {};
  },
  components: {
    LogOutButton,
    Theatre, // Register the LogOut component
  },
  methods: {},
  setup() {
    const username = ref("");

    onMounted(() => {
      console.log("admin dash mounted");
      const storedData = localStorage.getItem("identity");
      if (storedData) {
        const identityObject = JSON.parse(storedData);
        username.value = identityObject.username;
      }
    });

    return { username };
  },
};
</script>
