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
    <!-- Add a search bar for tags -->
    <div class="input-group mb-3">
      <input
        type="text"
        class="form-control py-2 rounded-pill mr-5 pr-5"
        placeholder="Search by tags"
        v-model="tagSearchQuery"
      />
      <button
        class="btn btn-outline-light text-dark border-0 rounded-pill ml-n5"
        @click="searchByTags"
      >
        Search
      </button>
    </div>

    <!-- Add a search bar for location -->
    <div class="input-group mb-3">
      <input
        type="text"
        class="form-control py-2 rounded-pill mr-1 pr-5"
        placeholder="Search by location"
        v-model="locationSearchQuery"
      />
      <button
        class="btn btn-outline-light text-dark border-0 rounded-pill ml-n5"
        @click="searchByLocation"
      >
        Search
      </button>
    </div>
    <div class="row">
      <div
        class="col-12 my-4"
        v-for="(venue, venueId) in venues"
        :key="venueId"
      >
        <!-- Skip rendering if no shows -->
        <div v-if="venue.shows.length > 0">
          <div class="card" style="width: 100%">
            <div class="card-body">
              <h5 class="card-title">{{ venue.vname }}</h5>
              <img
                :src="'http://localhost:8000' + venue.vimage_url"
                alt="Venue Image"
              /><br /><br />

              <h6 class="card-subtitle mb-2 text-muted">
                Location: {{ venue.vplace }}
              </h6>

              <!-- Show cards -->
              <div class="row">
                <div
                  class="col-md-6"
                  v-for="(show, showId) in venue.shows"
                  :key="showId"
                >
                  <div
                    class="my-4 mx-4 border border-2 border-secondary rounded-3"
                  >
                    <h6 class="card-subtitle mb-2 text-muted">
                      Show Name: {{ show.sname }}
                    </h6>
                    <p class="card-text">Tags: {{ show.stags }}</p>
                    <p class="card-text">Ticket Price: {{ show.sprice }}</p>
                    <p class="card-text">Show Timing: {{ show.time }}</p>

                    <!-- Conditional rendering for Book and Housefull buttons -->
                    <div v-if="show.seats - show.booked > 0">
                      <Book
                        :id="Number(showId)"
                        :show="show"
                        :venue="venue"
                        ref="bookModal"
                        @booking-confirmed="handleBookingConfirmed"
                      />
                    </div>
                    <div v-else type="button" class="btn btn-outline-danger">
                      Housefull
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import { onMounted, ref } from "vue";
import LogOutButton from "./Logout.vue";
import Book from "../components/Book.vue";

export default {
  name: "UserDash",

  components: {
    LogOutButton,
    Book,
  },

  data() {
    return {
      username: "",
      venues: [],
      tagSearchQuery: "",
      locationSearchQuery: "",
    };
  },

  methods: {
    async searchByTags() {
      try {
        const options = {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
          body: JSON.stringify({ tags: this.tagSearchQuery }),
        };

        const response = await fetch(
          "http://127.0.0.1:8000/tag_result",
          options
        );
        const data = await response.json();

        console.log("Search results by tags:", data);
        this.updateVenuesWithSearchResults(data);
      } catch (error) {
        console.error("Error searching by tags:", error);
      }
    },

    async searchByLocation() {
      try {
        const options = {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + localStorage.getItem("token"),
          },
          body: JSON.stringify({ location: this.locationSearchQuery }),
        };

        const response = await fetch(
          "http://127.0.0.1:8000/loc_result",
          options
        );
        const data = await response.json();

        console.log("Search results by location:", data);
        this.updateVenuesWithSearchResults(data);
      } catch (error) {
        console.error("Error searching by location:", error);
      }
    },

    updateVenuesWithSearchResults(searchResults) {
      this.venues = searchResults;
    },

    async fetchData() {
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

        const response = await fetch("http://127.0.0.1:8000/getVandS", options);
        const data = await response.json();

        console.log("got data from backend", data);
        this.venues = data;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },

    handleBookingConfirmed(bookingData) {
      console.log("Booking confirmed:", bookingData);
      const identityObject = JSON.parse(localStorage.getItem("identity"));

      const id = identityObject.id;

      fetch(`http://127.0.0.1:8000/book/${id}`, {
        method: "POST",
        body: JSON.stringify(bookingData),
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
      })
        .then((response) => {
          if (!response.ok) {
            console.log("Unsupported Media Type");
          }
          return response.json();
        })
        .then((data) => {
          console.log("Show Booked:", data);
          const options = {
            method: "GET",
            headers: {
              Authorization: "Bearer " + localStorage.getItem("token"),
            },
          };
          // fetch("http://127.0.0.1:8000/save_booking_time", {
          //     method: "POST",
          //     body: JSON.stringify(user),
          //     headers: {
          //       "Content-Type": "application/json",
          //     },
          //   }).catch((error) => {
          //     console.error("Fetch error:", error);
          //     // Handle the error or display it to the user
          //   });
          fetch("http://127.0.0.1:8000/getVandS", options)
            .then((response) => response.json())
            .then((data) => {
              console.log("from backend", data);
              this.venues = data;
            });
        });
    },
  },

  async mounted() {
    console.log("User Dashboard");
    await this.fetchData();
  },
};
</script>
