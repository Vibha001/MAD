<template>
  <div>
    <!-- Your logout button or link -->
    <button type="button" class="btn btn-link" @click="logout">Log Out</button>
  </div>
</template>

<script>
export default {
  name: "LogOut", // Changed from "Log-out" to "LogOut" for consistent naming
  methods: {
    logout() {
      // Remove the "token" and "role" items from localStorage
      localStorage.removeItem("token");
      localStorage.removeItem("role");
      localStorage.removeItem("identity");

      // Optionally, you can navigate the user to the login page or perform other actions
      // For example, if using Vue Router, you can navigate to the login page
      this.$router.push("/home"); // Replace "/login" with the actual login route
      this.$router.go(0);

      // Or you can trigger any other logic needed for logout
    },
  },
};
</script>
<style>
/* Style for the logout button */
.logout-button {
  background-color: #f44336; /* Red background color */
  color: white; /* White text color */
  border: none; /* Remove button border */
  padding: 10px 20px; /* Add padding to the button */
  cursor: pointer; /* Change cursor to a hand on hover */
}

/* Style for the logout button on hover */
.logout-button:hover {
  background-color: #d32f2f; /* Darker red background color on hover */
}
</style>
