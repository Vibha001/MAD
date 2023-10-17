<template>
  <form @submit.prevent="submit">
    <div role="alert" class="text-danger" v-if="error">
      {{ error_message }}
    </div>
    <div class="mx-auto col-10 col-md-8 col-lg-6">
      <div class="form-group">
        <label for="email">Enter Admin Email Address</label>
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
        <label for="email">Enter Admin Username </label>
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
        <label for="exampleInputPassword1">Enter Admin Password</label>
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
      <button class="btn btn-primary btn-lg btn-block" type="Submit">
        Register Admin
      </button>
    </div>
  </form>
</template>

<script>
export default {
  name: "AdminRegister",
  data() {
    return {
      email: "",
      password: "",
      username: "",
      error: false,
      error_message: "",
    };
  },
  methods: {
    submit: function submit() {
      let data = {
        email: this.email,
        password: this.password,
        username: this.username,
      };
      fetch("http://127.0.0.1:8000/admin_register", {
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
      this.$router.push("/admin");
    },
  },
};
</script>
