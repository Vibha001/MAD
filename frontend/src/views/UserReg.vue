<template>
  <form @submit.prevent="submit">
    <div class="mx-auto col-10 col-md-8 col-lg-6">
      <div class="form-group">
        <label for="email">Enter User Email Address</label>
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
    </div>
    <div class="mx-auto col-10 col-md-8 col-lg-6">
      <div class="form-group">
        <label for="email">Enter User Username </label>
        <input
          type="text"
          class="form-control mt-1"
          id="username"
          name="username"
          placeholder="Enter username"
          required
          v-model="username"
        />
      </div>
      <div class="form-group">
        <label for="exampleInputPassword1">Enter User Password</label>
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
        Register User
      </button>
    </div>
  </form>
</template>

<script setup>
// /* eslint-disable */
// import { ref } from "vue";
// // import axios from "axios";
// // import { useRouter } from "vue-router";

// // const email = ref("");
// // const password = ref("");
// // const username = ref("");
// // const router = useRouter();

// // const error = ref(false);
// // const error_message = ref("");

// // function onSubmit() {
// //   const url = "http://127.0.0.1:8080/user_register";
// //   const data = {
// //     email: email.value,
// //     password: password.value,
// //     username: username.value,
// //   };
// //   const config = {
// //     headers: {
// //       "Content-Type": "application/json",
// //     },
// //   };

// //   axios
// //     .post(url, data, config)
// //     .then((res) => {
// //       console.log(res);
// //       this.$r;
// //     })
// //     .catch((err) => {
// //       console.error(err);
// //       error.value = true;
// //       error_message.value = err.response.data.message;
// //     });
// // }
// //
//
</script>
<script>
export default {
  name: "UserRegister",
  data() {
    return {
      email: "",
      password: "",
      username: "",
    };
  },
  methods: {
    submit: function submit() {
      let data = {
        email: this.email,
        password: this.password,
        username: this.username,
      };
      fetch("http://127.0.0.1:8000/user_register", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then(function (response) {
          return response.json();
        })
        .then(function (rdata) {
          console.log(rdata);
          alert(rdata.message);
        });
      this.$router.push("/user");
    },
  },
};
</script>
