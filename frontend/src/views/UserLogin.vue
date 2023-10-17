<template>
  <form @submit.prevent="submit">
    <div class="text-danger" role="alert" v-if="error">
      {{ error_message }}
    </div>
    <div class="mx-auto col-10 col-md-8 col-lg-6">
      <div class="form-group">
        <label for="email">User Email Address</label>
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
        <label for="exampleInputPassword1">User Password</label>
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
      <router-link to="/user_reg">User</router-link>
    </h5>
  </form>
</template>

<script setup>
// /* eslint-disable */
// import { ref } from "vue";
// import axios from "axios";

// const email = ref("");
// const password = ref("");
// const error = ref(false);
// const error_message = ref("");

// function onSubmit() {
//   // alert(`${email.value} ${password.value}`);
//   const url = "http://127.0.0.1:8080/login";
//   const data = {
//     email: email.value,
//     password: password.value,
//   };
//   const config = {
//     headers: {
//       "Content-Type": "application/json",
//     },
//   };

//   axios
//     .post(url, data, config)
//     .then((res) => {
//       console.log(res);
//       localStorage.setItem("token", res.data.access_token);
//     })
//     .catch((err) => {
//       console.error(err);
//       error.value = true;
//       error_message.value = err.response.data.message;
//     });
// }
</script>
<script>
// import { onMounted } from "vue";

export default {
  name: "UserLogin",
  mounted() {
    console.log("user login mounted");
    const token = localStorage.getItem("token");
    if (token) {
      alert("Logout first");
      this.flag = true;
      // this.$router.push("/admin_dashboard");
    }
    if (this.flag && localStorage.getItem("role") === "user") {
      this.$router.push("/user_dashboard");
    }
    // } else {
    //   this.$router.push("/admin_login");
    // }
  },
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

      fetch("http://127.0.0.1:8000/login_user", {
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
            this.$router.push("/user_dashboard");
          } else {
            this.error = true;
            this.error_message = rdata.message;
          }
        });
    },
  },
};
</script>
