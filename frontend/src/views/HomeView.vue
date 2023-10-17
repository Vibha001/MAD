<template>
  <div class="home">
    <!-- <img alt="Vue logo" src="../assets/logo.png"> -->
    <!-- <HelloWorld msg="Welcome to Ticket Show App" /> -->
    <nav>
      <!-- <router-link to="/home"> Home </router-link> | -->
      <router-link to="/admin">Login as Admin</router-link> |
      <router-link to="/user">Login as User</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from "@/components/HelloWorld.vue";

export default {
  name: "HomeView",
  // components: {
  //   HelloWorld,
  // },
};
</script>
