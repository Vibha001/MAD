<template>
  <form @submit.prevent="submit">
    <div class="text-danger" role="alert" v-if="error">
      {{ error_message }}
    </div>
    <div class="mx-auto col-10 col-md-8 col-lg-6">
      <div class="form-group">
        <label for="email">Admin Email Address</label>
        <input
          type="email"
          class="form-control mt-1"
          id="email"
          name="email"
          placeholder="Enter email"
          required
          v-model="email"
        />
      </div>
      <div class="form-group">
        <label for="exampleInputPassword1">Admin Password</label>
        <input
          type="password"
          class="form-control mt-1"
          id="exampleInputPassword1"
          placeholder="Password"
          name="password"
          required
          v-model="password"
        />
      </div>
      <br />
      <button class="btn btn-primary btn-lg btn-block" type="submit">
        Login
      </button>
    </div>
    <br />
    <h5>
      Are you new here? Register as
      <router-link to="/admin_reg">Admin</router-link>
    </h5>
  </form>
</template>

<script>
import Vue from "vue"; // Import Vue
import VueRouter from "vue-router"; // Import Vue Router

Vue.use(VueRouter); // Use Vue Router

// import { onMounted } from "vue";
export default {
  name: "AdminLogin",
  // setup() {
  mounted() {
    console.log("admin login mounted");
    const token = localStorage.getItem("token");

    if (token) {
      alert("Logout first");
      this.flag = true;
      // this.$router.push("/admin_dashboard");
    }
    if (this.flag) {
      this.$router.push("/admin_dashboard");
    }
    // } else {
    //   this.$router.push("/admin_login");
    // }
  },
  // },
  data() {
    return {
      email: "",
      password: "",
      username: "",
      error: "",
      error_message: "",
    };
  },
  methods: {
    submit: function () {
      let data = {
        email: this.email,
        password: this.password,
        username: this.username,
      };

      // Initialize error and error_message
      // eslint-disable-next-line
      let error = false;
      // eslint-disable-next-line
      let error_message = "";

      fetch("http://127.0.0.1:8000/login_admin", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((rdata) => {
          console.log(rdata);

          if (rdata.access_token) {
            localStorage.setItem("token", rdata.access_token);
            localStorage.setItem("role", rdata.role);
            // Correct way to save data to localStorage
            localStorage.setItem(
              "identity",
              JSON.stringify({
                email: rdata.identity.email,
                id: rdata.identity.id,
                username: rdata.identity.username,
              })
            );
            const identityObject = JSON.parse(localStorage.getItem("identity"));

            // const id = identityObject.id;
            const data = { id: identityObject.id };
            fetch("http://127.0.0.1:8000/save_login_time", {
              method: "POST",
              body: JSON.stringify(data),
              headers: {
                "Content-Type": "application/json",
              },
            }).catch((error) => {
              console.error("Fetch error:", error);
              // Handle the error or display it to the user
            });
            // localStorage.setItem("identity", JSON.stringify(rdata.idenntity));
            this.$router.push("/admin_dashboard");
          } else {
            this.error = true;
            this.error_message = rdata.message;
          }
        });
    },
  },
};
</script>
