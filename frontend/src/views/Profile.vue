<template>
  <div class="container-fluid">
    <nav
      class="navbar navbar-expand-lg navbar-light bg-light fixed-top"
      style="font-size: 24px; padding: 20px"
    >
      <h4>{{ username }}'s Dashboard</h4>
      |
      <br />
      <router-link to="/user_dashboard"> User Dashboard </router-link> |<br />
      <router-link to="/bookings"> Bookings </router-link> |<br />
      <router-link to="/profile"> Profile </router-link> |<br />
      <LogOutButton />
    </nav>

    <div v-if="profileData">
      <h2>Username: {{ profileData.username }}</h2>
      <h2>Email: {{ profileData.email }}</h2>
      <h2>Role: {{ profileData.role }}</h2>
      <h2>Role Description: {{ profileData.role_descr }}</h2>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
</template>

<script>
import { onMounted, ref } from "vue";
import LogOutButton from "./Logout.vue";

export default {
  name: "Pro-file",

  components: {
    LogOutButton,
  },
  setup() {
    const username = ref("");
    const profileData = ref(null);
    const userId = ref(null);

    onMounted(async () => {
      console.log("User Profile");
      const storedData = localStorage.getItem("identity");
      if (storedData) {
        const identityObject = JSON.parse(storedData);
        username.value = identityObject.username;
        userId.value = identityObject.id;
      }

      try {
        const options = {
          method: "GET",
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        }; // Close the options object here

        const response = await fetch(
          `http://127.0.0.1:8000/profile/${userId.value}`,
          options
        );
        if (response.ok) {
          const data = await response.json();
          console.log("Profile From Backend");
          profileData.value = data;
        } else {
          console.error("Failed to fetch user profile data");
        }
      } catch (error) {
        console.error("Error fetching user profile data:", error);
      }
    });

    return { username, profileData };
  },
};
</script>
