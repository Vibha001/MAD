<template>
  <div id="app">
    <component :is="currentComponent" />
  </div>
</template>

<script>
import { onMounted, computed, watch } from "vue";
// import { computed } from "vue";
import HomeView from "./views/HomeView.vue";
import AdminDash from "./views/AdminDash.vue";
import UserDash from "./views/UserDash.vue";

export default {
  name: "AppV",
  components: { HomeView, AdminDash, UserDash },
  setup() {
    onMounted(() => {
      console.log("mounted");
      document.title = "Ticket Show";
    });

    const currentComponent = computed(() => {
      const token = localStorage.getItem("token");
      const role = localStorage.getItem("role");

      if (!token) {
        // No access token, render HomeView
        return "HomeView";
      } else {
        if (role === "admin") {
          // this.$router.go(0);
          return "AdminDash";
        } else {
          // this.$router.go(0);
          return "UserDash";
        }
      }
    });
    watch((currentComponent) => {
      if (
        currentComponent.value === "AdminDash" ||
        currentComponent.value === "UserDash"
      ) {
        // this.$router.go(0);
        // window.location.reload();
      }
    });
    return {
      currentComponent,
    };
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
