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

    <div>
      <div
        v-if="
          userData && userData.booked_shows && userData.booked_shows.length > 0
        "
      >
        <!-- Your booking card components here -->
        <div
          v-for="(booking, index) in userData.booked_shows"
          :key="index"
          class="booking-card"
        >
          <div class="card my-3 mx-3" style="width: 100%">
            <div class="card-body">
              <p class="card-text">
                <span class="Bold"
                  >{{ booking.venue.vname }} - {{ booking.show.sname }}</span
                >
                <span class="Bold">Show Timing: {{ booking.show.time }}</span>
                <span class="Bold">Price: {{ booking.price }}</span>
                <span class="Bold">Booked on: {{ booking.date }}</span>
                <span class="Bold">Ratings : {{ booking.show.srate }}</span>
              </p>
              <rate
                v-model="booking.show.srate"
                :maxStars="5"
                @rate="handleRating(booking.show.sid, $event)"
              />
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <p>No shows booked yet.</p>
      </div>
    </div>
  </div>
</template>

<script>
import LogOutButton from "./Logout.vue";
import Rate from "../components/Rate.vue";

export default {
  name: "Boo-kings",

  components: {
    LogOutButton,
    Rate,
  },

  data() {
    return {
      username: "",
      userData: [],
      identityObject: JSON.parse(localStorage.getItem("identity")),
    };
  },

  methods: {
    async handleRating(showId, rating) {
      console.log(rating);
      const options = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
        body: JSON.stringify({ rating: rating }),
      };

      try {
        const response = await fetch(
          `http://127.0.0.1:8000/rating/${showId}`,
          options
        );

        if (response.ok) {
          const data = await response.json();
          console.log("Rating added:", data);

          // After successfully adding the rating, fetch updated user data
          this.fetchUserData();
        } else {
          console.error("Failed to add rating");
        }
      } catch (error) {
        console.error("Error adding rating:", error);
      }
    },

    async fetchUserData() {
      try {
        const storedData = localStorage.getItem("identity");
        if (storedData) {
          const identityObject = JSON.parse(storedData);
          this.username = identityObject.username;
        }

        const options = {
          method: "GET",
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
        };

        const response = await fetch(
          `http://127.0.0.1:8000/user_booked_shows/${this.identityObject.id}`,
          options
        );

        if (response.ok) {
          const data = await response.json();
          console.log("got data from backend", data);
          this.userData = data;
        } else {
          console.error("Failed to fetch user data");
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
  },

  async mounted() {
    console.log("User Dashboard");
    await this.fetchUserData();
  },
};
</script>

<style scoped>
.card-text {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.Bold {
  font-weight: bold;
}
</style>
